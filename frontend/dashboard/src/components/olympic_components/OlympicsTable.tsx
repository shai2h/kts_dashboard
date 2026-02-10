import { OlympicsRow } from "@/types/olympics";

interface Props {
  rows: OlympicsRow[];
}

export default function OlympicsTable({ rows }: Props) {
  return (
    <div className="overflow-x-auto rounded-lg border">
      <table className="min-w-full text-sm">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-2 text-left">Микрогруппа</th>
            <th className="p-2">Отдел</th>
            <th className="p-2">Команда</th>
            <th className="p-2">Фигурное катание</th>
            <th className="p-2">Кёрлинг</th>
            <th className="p-2">Сноуборд</th>
            <th className="p-2">Хоккей %</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={`${r.microgroup}-${r.dept}`} className="border-t">
              <td className="p-2">{r.microgroup}</td>
              <td className="p-2 text-center">{r.dept}</td>
              <td className="p-2 text-center">{r.team}</td>
              <td className="p-2 text-center">{r.figure_skating ?? "-"}</td>
              <td className="p-2 text-center">{r.curling ?? "-"}</td>
              <td className="p-2 text-center">
                {r.snowboard ? r.snowboard.toLocaleString("ru-RU") : "-"}
              </td>
              <td className="p-2 text-center">
                {r.hockey_ratio !== null
                  ? `${(r.hockey_ratio * 100).toFixed(1)}%`
                  : "-"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
