"use client";

import * as React from "react";
import dynamic from "next/dynamic";
import type { OlympicsTeamAgg } from "@/types/olympics";
import { formatMoneyRu, formatPct } from "../shared/utils";
import type { SportMetricType } from "../shared/sports";


const Chart = dynamic(() => import("react-apexcharts"), { ssr: false });

type Props = {
    title: string;
    type: SportMetricType;
    teams: OlympicsTeamAgg[];
    metricKey: keyof OlympicsTeamAgg;
};

function fmt(val: number, type: SportMetricType) {
    if (type === "money") return formatMoneyRu(val);
    if (type === "ratio") return formatPct(val);
    return `${Math.trunc(val)}`;
}

const PALETTE = ["#259ffc", "#22c55e", "#f97316", "#a855f7", "#f43f5e"];

export default function SportTeamsVerticalBarChart({ title, type, teams, metricKey }: Props) {
    const safeTeams = Array.isArray(teams) ? teams : [];
    if (safeTeams[0]) console.log("sample value:", metricKey, safeTeams[0][metricKey]);
    const items = React.useMemo(() => {
        return [...safeTeams]
            .map((t) => ({
                team: t.team,
                value: (t[metricKey] as number | null) ?? null,
                total_accounts: t.total_accounts,
                bills_paid: t.bills_paid,
            }))
            .filter((x) => x.value !== null)
            .sort((a, b) => (b.value ?? 0) - (a.value ?? 0));
    }, [safeTeams, metricKey]);

    const teamColor = React.useMemo(() => {
        const uniqTeams = Array.from(new Set(items.map((i) => i.team))).sort();
        const map = new Map<string, string>();
        uniqTeams.forEach((team, idx) => map.set(team, PALETTE[idx % PALETTE.length]));
        return map;
    }, [items]);

    const colors = items.map((x) => teamColor.get(x.team) ?? PALETTE[0]);

    const categories = items.map((x) => x.team);
    const values = items.map((x) => x.value as number);



    const series = [{ name: title, data: values }];

    const options: ApexCharts.ApexOptions = {
        chart: { type: "bar", height: 520, toolbar: { show: false } },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: "45%",
                distributed: true,
                borderRadius: 8,
            },
        },
        colors,
        legend: { show: false },
        dataLabels: { enabled: true, formatter: (v) => fmt(Number(v), type), offsetY: -6 },
        xaxis: { categories, labels: { rotate: -15, trim: true, style: { colors: "#e5e7eb" } } },
        yaxis: { labels: { formatter: (v) => fmt(Number(v), type), style: { colors: "#e5e7eb" } } },
        tooltip: {
            custom: ({ dataPointIndex }) => {
                const it = items[dataPointIndex];
                if (!it) return "";
                const v = fmt(it.value as number, type);
                const extra =
                    type === "ratio"
                        ? `<div style="opacity:.75; margin-top:6px;">Счета: ${it.total_accounts}, оплачено: ${it.bills_paid}</div>`
                        : "";
                return `
          <div style="padding:10px; max-width:320px;">
            <div style="font-weight:600;">${it.team}</div>
            <div style="margin-top:8px;">${title}: <b>${v}</b></div>
            ${extra}
          </div>
        `;
            },
        },
        grid: { strokeDashArray: 4 },
    };

    return (
        <div className="rounded-xl border border-blue-400/35 bg-white/30 backdrop-blur-md p-4 text-white">
            <div className="mb-3">
                <div className="text-lg font-semibold text-[#259ffc]">{title}</div>
            </div>

            {items.length === 0 ? (
                <div className="py-10 text-sm text-muted-foreground">Нет данных для отображения</div>
            ) : (
                <>
                    <Chart options={options} series={series} type="bar" height={420} />

                    <div className="mt-3 flex flex-wrap gap-3 justify-center">
                        {items.map((it, idx) => (
                            <div key={it.team} className="flex items-center gap-2 text-sm">
                                <span className="inline-block h-3 w-3 rounded-sm" style={{ backgroundColor: colors[idx] }} />
                                <span className="text-gray-800">{it.team}</span>
                            </div>
                        ))}
                    </div>
                </>
            )}
        </div>
    );
}
