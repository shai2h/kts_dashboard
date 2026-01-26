import type { Metadata } from "next";
import { EcommerceMetrics } from "@/components/ecommerce/EcommerceMetrics";
import React from "react";
import MonthlyTarget from "@/components/ecommerce/MonthlyTarget";
import MonthlySalesChart from "@/components/ecommerce/MonthlySalesChart";
import StatisticsChart from "@/components/ecommerce/StatisticsChart";
import RecentOrders from "@/components/ecommerce/RecentOrders";
import DemographicCard from "@/components/ecommerce/DemographicCard";
import GorizontBar from "@/components/ecommerce/GorizontalBar";
import { EcommerceMetricsFact } from "@/components/ecommerce/EcommerceMetricsPlan";
import { EcommerceMetricsPlan } from "@/components/ecommerce/EcommerceMetricsFact";

import Image from "next/image";

export const metadata: Metadata = {
  title:
    "KTS - Dashboard | Главная",
  description: "Страница аналитических дашбордов отдела КТС",
};

export default function Ecommerce() {
  return (
    <div className="p-4 flex flex-col gap-6">

      {/* ВЕРХНИЙ БЛОК */}
      <div className="flex flex-col xl:flex-row gap-4 items-stretch">

        {/* ЛЕВАЯ ЧАСТЬ — 4 ПЛИТКИ */}
        <div className="flex flex-wrap gap-3 xl:w-1/2">

          {/* ПЛИТКИ */}
          <div className="w-full sm:w-[calc(50%-6px)] rounded-2xl border border-blue-200 shadow-xs bg-white p-6 flex flex-col justify-center min-h-[280px]">

            {/* ЛОГО + TITLE */}
            <div className="flex flex-col items-start gap-3 justify-center">
              <Image
                src="/logo.png"
                alt="Логотип"
                width={250}
                height={50}
              />
              <span className="text-2xl font-light text-gray-800">
                DASHBOARD ПРОДАЖИ
              </span>
            </div>

            {/* ДАТА */}
            <div className="mt-3 text-md text-blue-800 text-start">
              23 января 2026
            </div>

          </div>


          <div className="w-full sm:w-[calc(50%-6px)] min-h-[280px]">
            <MonthlyTarget />
          </div>

          <div className="w-full sm:w-[calc(50%-6px)] min-h-[200px]">
            <EcommerceMetricsPlan />
          </div>

          <div className="w-full sm:w-[calc(50%-6px)] min-h-[200px]">
            <EcommerceMetricsFact />
          </div>

        </div>

        {/* ПРАВАЯ ЧАСТЬ — ГРАФИК */}
        <div className="flex-1 flex rounded-2xl border bg-white  border-gray-200">
          <div className="w-full h-full">
            <GorizontBar />
          </div>
        </div>

      </div>

      {/* НИЖНИЙ БЛОК */}
      <div>
        <RecentOrders />
      </div>

    </div>
  );
}
