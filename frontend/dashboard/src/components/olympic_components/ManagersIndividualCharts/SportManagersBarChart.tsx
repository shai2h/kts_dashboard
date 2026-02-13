"use client";

import dynamic from "next/dynamic";
import { OlympicsRow } from "@/types/olympics";
import { formatMoneyRu, formatPct } from "../shared/utils";
import type { SportMetricType } from "../shared/sports";

const Chart = dynamic(() => import("react-apexcharts"), {
    ssr: false,
});

type Props = {
    title: string;
    type: SportMetricType;
    rows: OlympicsRow[];
    getValue: (r: OlympicsRow) => number | null;
    limit?: number | null;
};

export default function SportManagersBarChart({
    title,
    type,
    rows,
    getValue,
    limit = 29,
}: Props) {
    const items = rows
        .map((r) => {
            const v = getValue(r);
            return {
                label: r.microgroup,
                meta: `${r.dept} · ${r.team}`,
                value: v ?? 0,
            };
        })
        // .filter((x) => x.value !== null)
        .sort((a, b) => b.value - a.value);

    const categories = items.map((x) => x.label);

    // значения как есть (0 остаётся 0)
    const realValues = items.map((x) => x.value);

    // значения для отрисовки
    const EPS = type === "ratio" ? 0.0001 : type === "money" ? 0.01 : 0.0001;
    const plotValues = realValues.map((v) => (v === 0 ? EPS : v));

    const series = [{ name: title, data: plotValues }];

    const formatter = (val: number) => {
        if (type === "money") return formatMoneyRu(val);
        if (type === "ratio") return formatPct(val);
        return `${Math.trunc(val)}`;
    };

    const options: ApexCharts.ApexOptions = {
        chart: { type: "bar", height: 400, toolbar: { show: false } },
        plotOptions: {
            bar: { horizontal: true, barHeight: "70%" },
        },
        dataLabels: {
            enabled: true,
            formatter: (_val, opts) => {
                const real = realValues[opts.dataPointIndex] ?? 0;
                return formatter(real);
            },
        },
        xaxis: {
            categories,
            labels: { formatter: (v) => formatter(Number(v)) },
        },
        tooltip: {
            custom: ({ dataPointIndex }) => {
                const it = items[dataPointIndex];
                if (!it) return "";
                return `
          <div style="padding:10px; max-width:320px;">
            <div style="font-weight:600;">${it.label}</div>
            <div style="opacity:.75; margin-top:2px;">${it.meta}</div>
            <div style="margin-top:8px;">${title}: <b>${formatter(it.value as number)}</b></div>
          </div>
        `;
            },
        },
        grid: { strokeDashArray: 4 },
    };

    return (
        <div className="rounded-xl border border-blue-400/35 bg-white/30 backdrop-blur-md p-4 text-white">

            <div className="mb-3">
                <div className="text-lg font-bold font-semibold text-[#259ffc]">{title}</div>
            </div>

            {items.length === 0 ? (
                <div className="py-10 text-sm text-muted-foreground">Нет данных для отображения</div>
            ) : (
                <Chart options={options} series={series} type="bar" height={560} />
            )}
        </div>
    );
}
