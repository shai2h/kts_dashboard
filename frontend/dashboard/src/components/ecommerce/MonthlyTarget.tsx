"use client";

import dynamic from "next/dynamic";
import { ApexOptions } from "apexcharts";
import { useDashboard } from "@/hooks/useDashboard";

const ReactApexChart = dynamic(() => import("react-apexcharts"), {
  ssr: false,
});

export default function MonthlyTarget() {
  const { data, loading, error } = useDashboard();

  if (loading) {
    return <div>Загрузка...</div>;
  }

  if (error || !data) {
    return <div className="text-red-500">Ошибка загрузки данных</div>;
  }


  const series = [Number(data.total_percent.toFixed(1))];

  const options: ApexOptions = {
    colors: ["#465FFF"],
    chart: {
      fontFamily: "Outfit, sans-serif",
      type: "radialBar",
      height: 330,
      sparkline: { enabled: true },
    },
    plotOptions: {
      radialBar: {
        startAngle: -85,
        endAngle: 85,
        hollow: { size: "80%" },
        track: {
          background: "#E4E7EC",
          strokeWidth: "100%",
          margin: 5,
        },
        dataLabels: {
          name: { show: false },
          value: {
            fontSize: "36px",
            fontWeight: "600",
            offsetY: -40,
            formatter: (val) => `${val}%`,
          },
        },
      },
    },
    stroke: {
      lineCap: "round",
    },
  };

  return (
    <div className="rounded-2xl border border-gray-200 bg-white p-6 h-full">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">
        Процент выполнения плана
      </h3>

      <ReactApexChart
        options={options}
        series={series}
        type="radialBar"
        height={330}
        weight={330}
      />
    </div>
  );
}
