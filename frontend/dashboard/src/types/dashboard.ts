export interface DashboardTotal {
    total_plan: number;
    total_tec: number;
    total_percent: number;
}

export interface DashboardResponse extends DashboardTotal {
    by_podr: {
        podr: string;
        plan: number;
        tec: number;
        percent: number;
    }[];

    managers_by_podr: Record<
        string,
        {
            manager: string;
            plan: number;
            tec: number;
            percent: number;
        }[]
    >;
    quote: string;
}

interface ByPodrItem {
    podr: string;
    plan: number;
    tec: number;
    percent: number;
}
