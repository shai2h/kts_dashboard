import { DashboardResponse } from "@/types/dashboard";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function fetchDashboard(): Promise<DashboardResponse> {
    const res = await fetch(`${API_URL}/api/dashboard`, {
        cache: "no-store",
    });

    if (!res.ok) {
        throw new Error("Failed to fetch dashboard data");
    }

    return res.json();
}
