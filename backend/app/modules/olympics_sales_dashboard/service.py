from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, func, case
from .schemas import OlympicsTeamsIngestRequest

from .models import OlympicsRow, OlympicsTeamAgg
from .schemas import OlympicsIngestRequest

from .schemas import (
    OlympicsIngestRequest,
    OlympicsTeamsIngestRequest,
    OlympicsRowOut,
    OlympicsDeptOut,
    OlympicsDashboardResponse,
    OlympicsTeamOut,
)

# хелперы для данных, форматирование
# ---------- helpers ----------
def _clean_str(value: str | None) -> str | None:
    if not value:
        return None
    return value.replace("\u00A0", "").replace(" ", "").strip()


def parse_int(value: str | None) -> int | None:
    value = _clean_str(value)
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def parse_money(value: str | None) -> Decimal | None:
    value = _clean_str(value)
    if not value:
        return None
    value = value.replace(",", ".")
    try:
        return Decimal(value)
    except Exception:
        return None


# функция вставки данных в БД

async def ingest_olympics_data(
    session: AsyncSession,
    payload: OlympicsIngestRequest,
) -> dict:
    values: list[dict] = []

    for row in payload.rows:
        values.append({
            "microgroup": row.microgroup.strip(),
            "dept": row.dept.strip(),
            "team": row.team.strip(),

            "rop": row.rop.strip(),

            "figure_skating_count": row.figure_skating,
            "curling_count": row.curling,
            "snowboard_money": row.snowboard,

            "total_accounts": row.total_accounts,
            "bills_paid": row.bills_paid,

            "biathlon_count": row.biathlon,
            "freestyle_count": row.freestyle,
            "short_track_count": row.short_track,
            "ski_alpenism_count": row.ski_alpenism,

            "speed_skating_money": row.speed_skating,
            "bobsleigh_money": row.bobsleigh,

            "northern_combination_count": row.northern_combination,
            })

    stmt = insert(OlympicsRow).values(values)

    # поля, которые можно обновлять
    excluded = stmt.excluded

    update_map = {
        "figure_skating_count": func.coalesce(excluded.figure_skating_count, OlympicsRow.figure_skating_count),
        "curling_count": func.coalesce(excluded.curling_count, OlympicsRow.curling_count),
        "snowboard_money": func.coalesce(excluded.snowboard_money, OlympicsRow.snowboard_money),
        "total_accounts": func.coalesce(excluded.total_accounts, OlympicsRow.total_accounts),
        "bills_paid": func.coalesce(excluded.bills_paid, OlympicsRow.bills_paid),
        "biathlon_count": func.coalesce(excluded.biathlon_count, OlympicsRow.biathlon_count),
        "freestyle_count": func.coalesce(excluded.freestyle_count, OlympicsRow.freestyle_count),
        "short_track_count": func.coalesce(excluded.short_track_count, OlympicsRow.short_track_count),
        "ski_alpenism_count": func.coalesce(excluded.ski_alpenism_count, OlympicsRow.ski_alpenism_count),
        "speed_skating_money": func.coalesce(excluded.speed_skating_money, OlympicsRow.speed_skating_money),
        "bobsleigh_money": func.coalesce(excluded.bobsleigh_money, OlympicsRow.bobsleigh_money),
        "northern_combination_count": func.coalesce(
            excluded.northern_combination_count,
            OlympicsRow.northern_combination_count,
        ),
        "updated_at": func.now(),
    }

    stmt = stmt.on_conflict_do_update(
        constraint="uq_olympics_row_microgroup",
        set_=update_map,
    )

    result = await session.execute(stmt)
    await session.commit()

    return {
        "rows_received": len(payload.rows),
        "rows_processed": result.rowcount,
    }


TEAM_FIELDS = [
    "figure_skating", "curling", "snowboard", "hockey",
    "biathlon", "freestyle", "short_track", "ski_alpenism",
    "speed_skating", "bobsleigh", "northern_combination",
    "total_accounts", "bills_paid",
]

async def ingest_olympics_teams(session: AsyncSession, payload: OlympicsTeamsIngestRequest) -> dict:
    rows: list[dict] = []

    for r in payload.rows:
        d = r.model_dump()
        team = (d.get("team") or "").strip()
        if not team:
            continue
        d["team"] = team
        rows.append(d)

    if not rows:
        return {"status": "ok", "upserted": 0}

    stmt = insert(OlympicsTeamAgg).values(rows)
    excluded = stmt.excluded

    update_cols = {k: getattr(excluded, k) for k in TEAM_FIELDS}
    update_cols["updated_at"] = func.now()

    stmt = stmt.on_conflict_do_update(
        index_elements=[OlympicsTeamAgg.team],
        set_=update_cols,
    )

    await session.execute(stmt)
    await session.commit()

    return {"status": "ok", "upserted": len(rows)}

async def get_olympics_dashboard(session: AsyncSession) -> OlympicsDashboardResponse:
    # 1) строки по микрогруппам (индивидуалки)
    rows_stmt = select(
        OlympicsRow.microgroup,
        OlympicsRow.dept,
        OlympicsRow.team,

        OlympicsRow.figure_skating_count,
        OlympicsRow.curling_count,
        OlympicsRow.snowboard_money,

        OlympicsRow.biathlon_count,
        OlympicsRow.freestyle_count,
        OlympicsRow.short_track_count,
        OlympicsRow.ski_alpenism_count,

        OlympicsRow.speed_skating_money,
        OlympicsRow.bobsleigh_money,

        OlympicsRow.northern_combination_count,

        case(
            (
                OlympicsRow.total_accounts > 0,
                OlympicsRow.bills_paid / OlympicsRow.total_accounts,
            ),
            else_=None,
        ).label("hockey_ratio"),
    )

    rows_result = (await session.execute(rows_stmt)).all()

    rows = [
        OlympicsRowOut(
            microgroup=r.microgroup,
            dept=r.dept,
            team=r.team,

            figure_skating=r.figure_skating_count,
            curling=r.curling_count,
            snowboard=float(r.snowboard_money) if r.snowboard_money is not None else None,

            biathlon=r.biathlon_count,
            freestyle=r.freestyle_count,
            short_track=r.short_track_count,
            ski_alpenism=r.ski_alpenism_count,

            speed_skating=float(r.speed_skating_money) if r.speed_skating_money is not None else None,
            bobsleigh=float(r.bobsleigh_money) if r.bobsleigh_money is not None else None,

            northern_combination=r.northern_combination_count,
            hockey_ratio=float(r.hockey_ratio) if r.hockey_ratio is not None else None,
        )
        for r in rows_result
    ]

    # 2) by_team — ТОЛЬКО из таблицы агрегатов (olympics_team_agg)
    team_res = await session.execute(select(OlympicsTeamAgg))
    team_rows = team_res.scalars().all()

    by_team: list[OlympicsTeamOut] = []
    for t in team_rows:
        total = int(t.total_accounts or 0)
        paid = int(t.bills_paid or 0)
        ratio = (paid / total) if total > 0 else None

        by_team.append(
            OlympicsTeamOut(
                team=t.team,
                figure_skating=t.figure_skating,
                curling=t.curling,
                snowboard=float(t.snowboard) if t.snowboard is not None else None,
                hockey=float(t.hockey) if t.hockey is not None else None,  # <-- важно

                biathlon=t.biathlon,
                freestyle=t.freestyle,
                short_track=t.short_track,
                ski_alpenism=t.ski_alpenism,

                speed_skating=float(t.speed_skating) if t.speed_skating is not None else None,
                bobsleigh=float(t.bobsleigh) if t.bobsleigh is not None else None,
                northern_combination=t.northern_combination,

                total_accounts=total,
                bills_paid=paid,
                hockey_ratio=float(ratio) if ratio is not None else None,
            )
        )

    # 3) by_dept временно отключаем (но поле отдаём, чтобы фронт не падал)
    by_dept: list[OlympicsDeptOut] = []

    return OlympicsDashboardResponse(
        rows=rows,
        by_dept=by_dept,
        by_team=by_team,
    )