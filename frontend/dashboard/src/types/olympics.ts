export interface OlympicsRow {
  microgroup: string;
  dept: string;
  team: string;

  figure_skating: number | null;
  curling: number | null;
  snowboard: number | null;
  hockey_ratio: number | null;
}

export interface OlympicsDept {
  dept: string;

  figure_skating: number | null;
  curling: number | null;
  snowboard: number | null;
  hockey_ratio: number | null;
}

export interface OlympicsDashboardResponse {
  rows: OlympicsRow[];
  by_dept: OlympicsDept[];
}
