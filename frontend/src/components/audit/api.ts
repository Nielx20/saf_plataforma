const BASE_URL = import.meta.env.VITE_AUDIT_API_URL || "http://localhost:8000";

export interface TableInfo {
  name: string;
  row_count: number;
}

export interface ColumnSchema {
  column_name: string;
  data_type: string;
  is_nullable: "YES" | "NO";
  column_default: string | null;
}

export interface ForeignKeyInfo {
  column_name: string;
  foreign_table: string;
  foreign_column: string;
}

export interface TableSchema {
  columns: ColumnSchema[];
  foreign_keys: ForeignKeyInfo[];
  primary_key: string[];
}

export type RowValue = string | number | boolean | null | Record<string, unknown>;
export type Row = Record<string, RowValue>;

export interface TableDataResponse {
  columns: string[];
  rows: Row[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface OrphanIssue {
  table: string;
  column: string;
  references: string;
  orphan_count: number;
}

export interface OrphansResponse {
  issues: OrphanIssue[];
  checked_relations: number;
}

export interface IntegritySummary {
  total_tables: number;
  empty_tables: string[];
  tables_without_pk: string[];
  checked_relations: number;
  orphan_issues: OrphanIssue[];
}

export interface GetDataOptions {
  page?: number;
  pageSize?: number;
  search?: string;
  orderBy?: string;
  orderDir?: "asc" | "desc";
}

async function request<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Erro ${res.status}: ${body}`);
  }
  return res.json() as Promise<T>;
}

export const auditApi = {
  listTables: (): Promise<TableInfo[]> => request("/api/tables"),

  getSchema: (table: string): Promise<TableSchema> =>
    request(`/api/tables/${encodeURIComponent(table)}/schema`),

  getData: (
    table: string,
    { page = 1, pageSize = 50, search = "", orderBy = "", orderDir = "asc" }: GetDataOptions = {}
  ): Promise<TableDataResponse> => {
    const params = new URLSearchParams({
      page: String(page),
      page_size: String(pageSize),
    });
    if (search) params.set("search", search);
    if (orderBy) {
      params.set("order_by", orderBy);
      params.set("order_dir", orderDir);
    }
    return request(`/api/tables/${encodeURIComponent(table)}/data?${params.toString()}`);
  },

  getOrphans: (): Promise<OrphansResponse> => request("/api/integrity/orphans"),

  getSummary: (): Promise<IntegritySummary> => request("/api/integrity/summary"),
};