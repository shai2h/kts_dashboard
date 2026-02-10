import { fetchOlympicsDashboard } from "@/api/olympicsDashboard";
import OlympicsTable from "@/components/olympic_components/OlympicsTable";
import OlympicsDeptChart from "@/components/olympic_components/OlympicsDeptChart";

export default async function OlympicsPage() {
  const data = await fetchOlympicsDashboard();

  return (
    <div className="space-y-6 p-6">
      <h1 className="text-2xl font-semibold">
        Олимпиада продаж
      </h1>

      <OlympicsDeptChart data={data.by_dept} />

      <OlympicsTable rows={data.rows} />
    </div>
  );
}
