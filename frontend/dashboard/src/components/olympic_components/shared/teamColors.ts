const PALETTE = ["#259ffc", "#22c55e", "#f97316", "#a855f7", "#f43f5e"];

export function colorForTeam(team: string): string {
    let hash = 0;
    for (let i = 0; i < team.length; i++) hash = (hash * 31 + team.charCodeAt(i)) >>> 0;
    return PALETTE[hash % PALETTE.length];
}
