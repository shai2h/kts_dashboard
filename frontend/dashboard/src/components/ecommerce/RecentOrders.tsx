"use client";

import {
  Table,
  TableBody,
  TableCell,
  TableHeader,
  TableRow,
} from "../ui/table";
import Image from "next/image";
import { useDashboard } from "@/hooks/useDashboard";

export default function ManagersByDepartment() {
  const { data, loading } = useDashboard();

  if (loading || !data) return null;

  return (
    <div className="grid grid-cols-3 gap-4">
      {Object.entries(data.managers_by_podr as Record<string, ManagerStat[]>)
        .map(([podr, managers]) => (
          <div
            key={podr}
            className="rounded-2xl border border-gray-200 shadow-xs bg-white p-6"
          >
            {/* Заголовок подразделения */}
            <div className="mb-3 flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-[#1b038b]" />
              <h3 className="text-xl font-medium text-gray-700">
                {podr}
              </h3>
            </div>

            {/* Таблица */}
            <Table>
              <TableHeader>
                <TableRow>
                  <TableCell isHeader className="text-xs text-gray-400">
                    Менеджер
                  </TableCell>
                  <TableCell
                    isHeader
                    className="text-xs text-gray-400 text-right"
                  >
                    %
                  </TableCell>
                </TableRow>
              </TableHeader>

              <TableBody>
                {[...managers]
                  .sort((a, b) => b.percent - a.percent)
                  .map((m, idx) => (
                    <TableRow key={idx}>
                      <TableCell>
                        <div className="flex items-center gap-3">
                          <span className="text-sm text-gray-800 leading-tight">
                            {m.manager}
                          </span>
                        </div>
                      </TableCell>

                      <TableCell
                        className={`text-right font-medium ${m.percent >= 100
                          ? "text-green-600"
                          : m.percent < 50
                            ? "text-red-500"
                            : "text-gray-700"
                          }`}
                      >
                        {m.percent.toFixed(1)}%
                      </TableCell>
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          </div>
        ))}
    </div>
  );
}
