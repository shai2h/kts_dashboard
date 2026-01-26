"use client";

import React from "react";
import { RubleIcon, PlanIcon } from "@/icons";
import { formatNumber } from "@/lib/format";
import { useDashboard } from "@/hooks/useDashboard";


export const EcommerceMetrics = () => {
  const { data, loading, error } = useDashboard();

  if (loading) {
    return <div>Загрузка...</div>;
  }

  if (error || !data) {
    return <div className="text-red-500">Ошибка загрузки данных</div>;
  }

  return (
    <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 md:gap-6">
      {/* Общий план */}
      <div className="rounded-2xl border border-gray-200 bg-white p-5 md:p-6 max-w-xs">
        <div className="flex items-center justify-center w-12 h-12 bg-blue-400 rounded-xl">
          <PlanIcon className="size-6 text-white" />
        </div>

        <div className="mt-5">
          <span className="text-sm text-gray-500">
            Общий план
          </span>
          <h4 className="mt-2 font-bold text-gray-800 text-title-sm">
            {formatNumber(data.total_plan)} ₽
          </h4>
        </div>
      </div>

      {/* Общий факт */}
      <div className="rounded-2xl border border-gray-200 bg-white p-5 md:p-6 max-w-xs">
        <div className="flex items-center justify-center w-12 h-12 bg-blue-400 rounded-xl">
          <RubleIcon className="size-6 text-white" />
        </div>

        <div className="mt-5">
          <span className="text-sm text-gray-500">
            Общий факт
          </span>
          <h4 className="mt-2 font-bold text-gray-800 text-title-sm">
            {formatNumber(data.total_tec)} ₽
          </h4>
        </div>
      </div>
    </div>
  );
};
