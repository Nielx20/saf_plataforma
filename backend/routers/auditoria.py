"""
Router de Auditoria do Banco de Dados
--------------------------------------
Reaproveita o `engine` do seu database.py (SQLAlchemy) para introspectar o
schema 'public' do Postgres e checar integridade referencial.

Para plugar no seu main.py:

    from routers import calculos, clientes, anamnese, auditoria

    app.include_router(auditoria.router)
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.engine import Row

from database import engine

router = APIRouter(prefix="/api", tags=["auditoria"])


def _rows_to_dicts(rows) -> list[dict]:
    return [dict(r._mapping) for r in rows]


def _table_exists(conn, table_name: str) -> bool:
    result = conn.execute(
        text(
            """
            SELECT 1 FROM information_schema.tables
            WHERE table_schema = 'public' AND table_name = :table_name
            """
        ),
        {"table_name": table_name},
    )
    return result.first() is not None


@router.get("/tables")
def list_tables():
    """Lista todas as tabelas do schema public com contagem de linhas."""
    with engine.connect() as conn:
        tables = [
            r[0]
            for r in conn.execute(
                text(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                    ORDER BY table_name;
                    """
                )
            )
        ]
        result = []
        for t in tables:
            count = conn.execute(text(f'SELECT COUNT(*) FROM "{t}"')).scalar()
            result.append({"name": t, "row_count": count})
        return result


@router.get("/tables/{table_name}/schema")
def table_schema(table_name: str):
    """Retorna colunas, chave primária e chaves estrangeiras da tabela."""
    with engine.connect() as conn:
        if not _table_exists(conn, table_name):
            raise HTTPException(404, "Tabela não encontrada")

        columns = _rows_to_dicts(
            conn.execute(
                text(
                    """
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns
                    WHERE table_schema = 'public' AND table_name = :table_name
                    ORDER BY ordinal_position;
                    """
                ),
                {"table_name": table_name},
            )
        )

        fks = _rows_to_dicts(
            conn.execute(
                text(
                    """
                    SELECT
                        kcu.column_name,
                        ccu.table_name AS foreign_table,
                        ccu.column_name AS foreign_column
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                        ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage ccu
                        ON tc.constraint_name = ccu.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY'
                        AND tc.table_schema = 'public' AND tc.table_name = :table_name;
                    """
                ),
                {"table_name": table_name},
            )
        )

        pk = [
            r[0]
            for r in conn.execute(
                text(
                    """
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                        ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.constraint_type = 'PRIMARY KEY'
                        AND tc.table_schema = 'public' AND tc.table_name = :table_name;
                    """
                ),
                {"table_name": table_name},
            )
        ]

        return {"columns": columns, "foreign_keys": fks, "primary_key": pk}


@router.get("/tables/{table_name}/data")
def table_data(
    table_name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=500),
    search: Optional[str] = None,
    order_by: Optional[str] = None,
    order_dir: str = Query("asc", regex="^(asc|desc)$"),
):
    """Consulta paginada, com busca livre nas colunas de texto e ordenação opcional."""
    with engine.connect() as conn:
        if not _table_exists(conn, table_name):
            raise HTTPException(404, "Tabela não encontrada")

        cols = _rows_to_dicts(
            conn.execute(
                text(
                    """
                    SELECT column_name, data_type FROM information_schema.columns
                    WHERE table_schema = 'public' AND table_name = :table_name
                    """
                ),
                {"table_name": table_name},
            )
        )
        col_names = [c["column_name"] for c in cols]
        text_cols = [
            c["column_name"]
            for c in cols
            if c["data_type"] in ("text", "character varying", "character")
        ]

        where_clause = ""
        params: dict = {}
        if search and text_cols:
            conditions = " OR ".join(
                f'"{c}"::text ILIKE :search' for c in text_cols
            )
            where_clause = f"WHERE {conditions}"
            params["search"] = f"%{search}%"

        order_clause = ""
        if order_by and order_by in col_names:
            safe_dir = "ASC" if order_dir == "asc" else "DESC"
            order_clause = f'ORDER BY "{order_by}" {safe_dir}'

        offset = (page - 1) * page_size

        total = conn.execute(
            text(f'SELECT COUNT(*) FROM "{table_name}" {where_clause}'), params
        ).scalar()

        rows = _rows_to_dicts(
            conn.execute(
                text(
                    f'SELECT * FROM "{table_name}" {where_clause} {order_clause} '
                    f"LIMIT :limit OFFSET :offset"
                ),
                {**params, "limit": page_size, "offset": offset},
            )
        )

        return {
            "columns": col_names,
            "rows": rows,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }


def _fetch_orphans(conn) -> tuple[list[dict], int]:
    fks = _rows_to_dicts(
        conn.execute(
            text(
                """
                SELECT
                    tc.table_name,
                    kcu.column_name,
                    ccu.table_name AS foreign_table,
                    ccu.column_name AS foreign_column
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage ccu
                    ON tc.constraint_name = ccu.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema = 'public';
                """
            )
        )
    )

    issues = []
    for fk in fks:
        table, col = fk["table_name"], fk["column_name"]
        ftable, fcol = fk["foreign_table"], fk["foreign_column"]
        count = conn.execute(
            text(
                f'''
                SELECT COUNT(*) FROM "{table}" t
                WHERE t."{col}" IS NOT NULL
                AND NOT EXISTS (
                    SELECT 1 FROM "{ftable}" f WHERE f."{fcol}" = t."{col}"
                )
                '''
            )
        ).scalar()
        if count > 0:
            issues.append(
                {
                    "table": table,
                    "column": col,
                    "references": f"{ftable}.{fcol}",
                    "orphan_count": count,
                }
            )
    return issues, len(fks)


@router.get("/integrity/orphans")
def check_orphans():
    """Verifica registros cuja FK aponta para um valor inexistente na tabela referenciada."""
    with engine.connect() as conn:
        issues, total_fks = _fetch_orphans(conn)
        return {"issues": issues, "checked_relations": total_fks}


@router.get("/integrity/summary")
def integrity_summary():
    """Resumo geral: tabelas vazias, tabelas sem PK e FKs órfãs."""
    with engine.connect() as conn:
        tables = [
            r[0]
            for r in conn.execute(
                text(
                    """
                    SELECT table_name FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                    """
                )
            )
        ]

        empty_tables = []
        tables_without_pk = []

        for t in tables:
            count = conn.execute(text(f'SELECT COUNT(*) FROM "{t}"')).scalar()
            if count == 0:
                empty_tables.append(t)

            pk_count = conn.execute(
                text(
                    """
                    SELECT COUNT(*) FROM information_schema.table_constraints
                    WHERE constraint_type = 'PRIMARY KEY'
                        AND table_schema = 'public' AND table_name = :table_name
                    """
                ),
                {"table_name": t},
            ).scalar()
            if pk_count == 0:
                tables_without_pk.append(t)

        issues, total_fks = _fetch_orphans(conn)

        return {
            "total_tables": len(tables),
            "empty_tables": empty_tables,
            "tables_without_pk": tables_without_pk,
            "checked_relations": total_fks,
            "orphan_issues": issues,
        }