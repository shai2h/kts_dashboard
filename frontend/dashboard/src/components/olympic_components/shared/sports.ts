export type SportMetricType = "count" | "money" | "ratio";

export type OlympicsMetricsShape = {
    figure_skating: number | null;
    curling: number | null;
    snowboard: number | null;

    biathlon: number | null;
    freestyle: number | null;
    short_track: number | null;
    ski_alpenism: number | null;

    speed_skating: number | null;
    bobsleigh: number | null;

    northern_combination: number | null;
    hockey_ratio: number | null;
};

export const SPORTS: Array<{
    key: keyof OlympicsMetricsShape;
    title: string;
    type: SportMetricType;
    getValue: (r: OlympicsMetricsShape) => number | null;
}> = [
        { key: "figure_skating", title: "Фигурное катание (клиенты)", type: "count", getValue: (r) => r.figure_skating },
        { key: "curling", title: "Кёрлинг (бренды)", type: "count", getValue: (r) => r.curling },
        { key: "snowboard", title: "Сноуборд (ДС)", type: "money", getValue: (r) => r.snowboard },
        { key: "hockey_ratio", title: "Хоккей (конверсия)", type: "ratio", getValue: (r) => r.hockey_ratio },

        { key: "biathlon", title: "Биатлон (Интерколд + ПР)", type: "count", getValue: (r) => r.biathlon },
        { key: "freestyle", title: "Фристайл (Rosso)", type: "count", getValue: (r) => r.freestyle },
        { key: "short_track", title: "Шорт-трек (итальянские бренды)", type: "count", getValue: (r) => r.short_track },
        { key: "ski_alpenism", title: "Ски-альпинизм (100% оплата+отгрузка)", type: "count", getValue: (r) => r.ski_alpenism },

        { key: "speed_skating", title: "Конькобежный спорт (сумма 100/100)", type: "money", getValue: (r) => r.speed_skating },
        { key: "bobsleigh", title: "Бобслей (сумма реализаций)", type: "money", getValue: (r) => r.bobsleigh },

        { key: "northern_combination", title: "Северная комбинация (счета с движением)", type: "count", getValue: (r) => r.northern_combination },
    ];
