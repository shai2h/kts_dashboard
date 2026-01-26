"use client";

import { useEffect, useState } from "react";
import { fetchDashboard } from "@/lib/api/dashboard";
import { DashboardResponse } from "@/types/dashboard";



export function useDashboard() {
    const [data, setData] = useState<DashboardResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetchDashboard()
            .then(setData)
            .catch((err) => setError(err.message))
            .finally(() => setLoading(false));
    }, []);

    return { data, loading, error };
}
