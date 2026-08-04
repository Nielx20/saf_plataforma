import { useEffect, useState, useCallback, type ReactElement, type ReactNode } from "react";
import { auditApi } from "./api";
import type {
  TableInfo,
  TableDataResponse,
  IntegritySummary,
  RowValue,
} from "./api";
import "./DataAuditScreen.css";

type Tab = "dados" | "integridade";

export default function DataAuditScreen(): ReactElement {
  const [tab, setTab] = useState<Tab>("dados");
  const [tables, setTables] = useState<TableInfo[]>([]);
  const [selectedTable, setSelectedTable] = useState<string>("");
  const [tablesLoading, setTablesLoading] = useState<boolean>(true);
  const [tablesError, setTablesError] = useState<string | null>(null);

  useEffect(() => {
    auditApi
      .listTables()
      .then((data) => {
        setTables(data);
        if (data.length > 0) setSelectedTable(data[0].name);
      })
      .catch((err: Error) => setTablesError(err.message))
      .finally(() => setTablesLoading(false));
  }, []);

  return (
    <div className="audit-screen">
      <header className="audit-header">
        <h1>Auditoria do Banco de Dados</h1>
        <nav className="audit-tabs">
          <button
            className={tab === "dados" ? "active" : ""}
            onClick={() => setTab("dados")}
          >
            Dados
          </button>
          <button
            className={tab === "integridade" ? "active" : ""}
            onClick={() => setTab("integridade")}
          >
            Integridade
          </button>
        </nav>
      </header>

      {tablesLoading && <p className="audit-info">Carregando tabelas...</p>}
      {tablesError && <p className="audit-error">Erro ao carregar tabelas: {tablesError}</p>}

      {!tablesLoading && !tablesError && tab === "dados" && (
        <DataTab
          tables={tables}
          selectedTable={selectedTable}
          onSelectTable={setSelectedTable}
        />
      )}

      {!tablesLoading && !tablesError && tab === "integridade" && <IntegrityTab />}
    </div>
  );
}

interface DataTabProps {
  tables: TableInfo[];
  selectedTable: string;
  onSelectTable: (table: string) => void;
}

function DataTab({ tables, selectedTable, onSelectTable }: DataTabProps): ReactElement {
  const [data, setData] = useState<TableDataResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState<string>("");
  const [page, setPage] = useState<number>(1);
  const [orderBy, setOrderBy] = useState<string>("");
  const [orderDir, setOrderDir] = useState<"asc" | "desc">("asc");

  const load = useCallback(() => {
    if (!selectedTable) return;
    setLoading(true);
    setError(null);
    auditApi
      .getData(selectedTable, { page, pageSize: 50, search, orderBy, orderDir })
      .then(setData)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, [selectedTable, page, search, orderBy, orderDir]);

  useEffect(() => {
    setPage(1);
  }, [selectedTable, search]);

  useEffect(() => {
    load();
  }, [load]);

  const toggleSort = (col: string) => {
    if (orderBy === col) {
      setOrderDir(orderDir === "asc" ? "desc" : "asc");
    } else {
      setOrderBy(col);
      setOrderDir("asc");
    }
  };

  return (
    <div className="audit-panel">
      <div className="audit-controls">
        <select value={selectedTable} onChange={(e) => onSelectTable(e.target.value)}>
          {tables.map((t) => (
            <option key={t.name} value={t.name}>
              {t.name} ({t.row_count} registros)
            </option>
          ))}
        </select>
        <input
          type="text"
          placeholder="Buscar..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {loading && <p className="audit-info">Carregando dados...</p>}
      {error && <p className="audit-error">Erro: {error}</p>}

      {data && !loading && (
        <>
          <div className="audit-table-wrap">
            <table className="audit-table">
              <thead>
                <tr>
                  {data.columns.map((col) => (
                    <th key={col} onClick={() => toggleSort(col)}>
                      {col}
                      {orderBy === col ? (orderDir === "asc" ? " ▲" : " ▼") : ""}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.rows.map((row, i) => (
                  <tr key={i}>
                    {data.columns.map((col) => (
                      <td key={col}>{formatValue(row[col])}</td>
                    ))}
                  </tr>
                ))}
                {data.rows.length === 0 && (
                  <tr>
                    <td colSpan={data.columns.length} className="audit-empty">
                      Nenhum registro encontrado.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          <div className="audit-pagination">
            <button disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
              Anterior
            </button>
            <span>
              Página {data.page} de {Math.max(data.total_pages, 1)} — {data.total} registros
            </span>
            <button
              disabled={page >= data.total_pages}
              onClick={() => setPage((p) => p + 1)}
            >
              Próxima
            </button>
          </div>
        </>
      )}
    </div>
  );
}

function IntegrityTab(): ReactElement | null {
  const [summary, setSummary] = useState<IntegritySummary | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    auditApi
      .getSummary()
      .then(setSummary)
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p className="audit-info">Rodando checagens de integridade...</p>;
  if (error) return <p className="audit-error">Erro: {error}</p>;
  if (!summary) return null;

  const hasIssues =
    summary.empty_tables.length > 0 ||
    summary.tables_without_pk.length > 0 ||
    summary.orphan_issues.length > 0;

  return (
    <div className="audit-panel">
      <div className="audit-cards">
        <div className="audit-card">
          <span className="audit-card-value">{summary.total_tables}</span>
          <span className="audit-card-label">Tabelas no schema</span>
        </div>
        <div className="audit-card">
          <span className="audit-card-value">{summary.checked_relations}</span>
          <span className="audit-card-label">Relações (FKs) checadas</span>
        </div>
        <div className={`audit-card ${summary.orphan_issues.length > 0 ? "warn" : "ok"}`}>
          <span className="audit-card-value">{summary.orphan_issues.length}</span>
          <span className="audit-card-label">Relações com registros órfãos</span>
        </div>
      </div>

      {!hasIssues && (
        <p className="audit-ok-message">
          Nenhum problema encontrado: sem tabelas vazias, sem tabelas sem chave primária e sem
          registros órfãos.
        </p>
      )}

      {summary.tables_without_pk.length > 0 && (
        <section className="audit-issue-section">
          <h3>Tabelas sem chave primária</h3>
          <ul>
            {summary.tables_without_pk.map((t) => (
              <li key={t}>{t}</li>
            ))}
          </ul>
        </section>
      )}

      {summary.empty_tables.length > 0 && (
        <section className="audit-issue-section">
          <h3>Tabelas vazias</h3>
          <ul>
            {summary.empty_tables.map((t) => (
              <li key={t}>{t}</li>
            ))}
          </ul>
        </section>
      )}

      {summary.orphan_issues.length > 0 && (
        <section className="audit-issue-section">
          <h3>Registros órfãos (FK apontando para valor inexistente)</h3>
          <table className="audit-table">
            <thead>
              <tr>
                <th>Tabela</th>
                <th>Coluna</th>
                <th>Referencia</th>
                <th>Qtd. órfãos</th>
              </tr>
            </thead>
            <tbody>
              {summary.orphan_issues.map((issue, i) => (
                <tr key={i}>
                  <td>{issue.table}</td>
                  <td>{issue.column}</td>
                  <td>{issue.references}</td>
                  <td className="audit-warn-text">{issue.orphan_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      )}
    </div>
  );
}

function formatValue(value: RowValue): ReactNode {
  if (value === null || value === undefined) return <span className="audit-null">null</span>;
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}
