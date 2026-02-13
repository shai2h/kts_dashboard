import { OlympicsDashboardResponse } from "@/types/olympics";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function fetchOlympicsDashboard(): Promise<OlympicsDashboardResponse> {
    const res = await fetch(`${API_URL}/api/v1/olympics/dashboard`, {
        cache: "no-store",
    });

    if (!res.ok) {
        const text = await res.text().catch(() => "");
        console.error("Olympics dashboard fetch failed:", res.status, text);
        throw new Error("Failed to fetch olympics dashboard");
    }

    const json = (await res.json()) as any;

    // ключевая диагностика:
    console.log("OLYMPICS JSON keys:", Object.keys(json));
    console.log("by_team isArray:", Array.isArray(json.by_team), "len:", json.by_team?.length);
    console.log("by_team sample:", json.by_team?.[0]);

    return json as OlympicsDashboardResponse;
}
