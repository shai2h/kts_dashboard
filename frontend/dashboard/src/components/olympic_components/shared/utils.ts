export function formatMoneyRu(value: number) {
    return new Intl.NumberFormat("ru-RU", {
        maximumFractionDigits: 0,
    }).format(value);
}

export function formatPct(value01: number) {
    return `${(value01 * 100).toFixed(1)}%`;
}