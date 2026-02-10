"use client";

import Chart from "react-apexcharts";
import { OlympicsDept } from "@/types/olympics";

interface Props {
  data: OlympicsDept[];
}

export default function OlympicsDeptChart({ data }: Props) {
  const series = [
    {
      name: "Сноуборд",
      data: data.map((d) => d.snowboard ?? 0),
    },
  ];

  const options: ApexCharts.ApexOptions = {
    chart: {
      type: "bar",
      height: 350,
    },
    xaxis: {
      categories: data.map((d) => d.dept),
    },
    dataLabels: {
      enabled: false,
    },
    title: {
      text: "Поступление ДС по отделам (Сноуборд)",
    },
  };

  return (
    <div className="rounded-lg border p-4">
      <Chart options={options} series={series} type="bar" height={350} />
    </div>
  );
}
