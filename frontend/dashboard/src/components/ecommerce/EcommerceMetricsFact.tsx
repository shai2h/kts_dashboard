"use client";

import React from "react";
import { BoxIconLine, TableIcon } from "@/icons";
import { formatNumber } from "@/lib/format";
import { useDashboard } from "@/hooks/useDashboard";


export const EcommerceMetricsPlan = () => {
    const { data, loading, error } = useDashboard();

    if (loading) {
        return <div className="rounded-2xl border border-gray-200 bg-gray-50 p-6 min-h-[180px] flex items-center justify-center">Загрузка...</div>;
    }

    if (error || !data) {
        return <div className="rounded-2xl border border-red-200 bg-red-50 p-6 text-red-500 min-h-[180px] flex items-center justify-center">Ошибка</div>;
    }

    return (
        <div className="rounded-2xl border border-gray-200 bg-white p-6 h-full">
            <div className="flex items-center justify-center w-12 h-12 bg-blue-500 rounded-xl">
                <TableIcon className="size-6 text-white" />
            </div>

            <div className="mt-5">
                <span className="text-sm text-gray-500">
                    Общий план
                </span>
                <h4 className="mt-2 font-bold text-gray-800 text-xl sm:text-2xl">
                    {formatNumber(data.total_plan)} ₽
                </h4>
            </div>
        </div>
    );
};