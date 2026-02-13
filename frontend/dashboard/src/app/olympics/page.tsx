import { fetchOlympicsDashboard } from "@/api/olympicsDashboard";
import OlympicsSportsCarousel from "@/components/olympic_components/ManagersIndividualCharts/OlympicsSportsCarousel";
import OlympicsTeamsCarousel from "@/components/olympic_components/TeamsCharts/OlympicsTeamsCarousel";





export default async function OlympicsPage() {
  const data = await fetchOlympicsDashboard();

  return (
    <div
      className="min-h-screen"
      style={{
        backgroundImage: "url(/bg_olympic.png)",
        backgroundSize: "cover",
        backgroundRepeat: "no-repeat",
      }}
    >

      <div className="min-h-screen">
        <div className="p-6 space-y-6">
          <h1 className="
            inline-block
            text-3xl font-semibold
            text-[#0b2a4a]
            px-4 py-2
            rounded-xl
            bg-white/70
            backdrop-blur-md
            shadow-lg
          ">
            И снова... Быстрее! Выше! Сильнее!
          </h1>
          <OlympicsSportsCarousel rows={data.rows} />
        </div>
        <div className="p-6 space-y-6">
          <OlympicsTeamsCarousel teams={data.by_team ?? []} />
        </div>


      </div>
    </div>
  );
}
