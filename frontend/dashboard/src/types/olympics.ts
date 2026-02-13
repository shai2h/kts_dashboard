export interface OlympicsRow {
  microgroup: string;
  dept: string;
  team: string;

  figure_skating: number | null;
  curling: number | null;
  snowboard: number | null;

  biathlon: number | null;
  freestyle: number | null;
  short_track: number | null;
  ski_alpenism: number | null;

  speed_skating: number | null;
  bobsleigh: number | null;

  northern_combination: number | null;

  hockey_ratio: number | null; // 0..1
}

export interface OlympicsDeptAgg {
  dept: string;

  figure_skating: number | null;
  curling: number | null;
  snowboard: number | null;

  biathlon: number | null;
  freestyle: number | null;
  short_track: number | null;
  ski_alpenism: number | null;

  speed_skating: number | null;
  bobsleigh: number | null;

  northern_combination: number | null;

  total_accounts: number;
  bills_paid: number;
  hockey_ratio: number | null;
}

export interface OlympicsTeamAgg {
  team: string;

  figure_skating: number | null;
  curling: number | null;
  snowboard: number | null;

  biathlon: number | null;
  freestyle: number | null;
  short_track: number | null;
  ski_alpenism: number | null;

  speed_skating: number | null;
  bobsleigh: number | null;

  northern_combination: number | null;

  total_accounts: number;
  bills_paid: number;
  hockey_ratio: number | null;
}

export interface OlympicsDashboardResponse {
  rows: OlympicsRow[];
  by_dept: OlympicsDeptAgg[];
  by_team: OlympicsTeamAgg[];
}
