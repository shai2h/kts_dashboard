import { OlympicsDashboardResponse } from "@/types/olympics";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function fetchOlympicsDashboard(): Promise<OlympicsDashboardResponse> {
  const res = await fetch(`${API_URL}/api/v1/olympics/dashboard`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error("Failed to fetch olympics dashboard");
  }

  return res.json();
}
