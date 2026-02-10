from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, func, case

from .models import OlympicsRow
from .schemas import OlympicsIngestRequest

from .schemas import (
    OlympicsRowOut,
    OlympicsDeptOut,
    OlympicsDashboardResponse,
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
        values.append(
            {
                "microgroup": row.microgroup,
                "dept": row.dept,
                "team": row.team,

                "figure_skating_count": parse_int(row.figure_skating),
                "curling_count": parse_int(row.curling),
                "snowboard_money": parse_money(row.snowboard),

                "total_accounts": parse_int(row.total_accounts),
                "bills_paid": parse_int(row.bills_paid),

                "biathlon_count": parse_int(row.biathlon),
                "freestyle_count": parse_int(row.freestyle),
                "short_track_count": parse_int(row.short_track),
                "ski_alpenism_count": parse_int(row.ski_alpenism),

                "speed_skating_money": parse_money(row.speed_skating),
                "bobsleigh_money": parse_money(row.bobsleigh),

                "northern_combination_count": parse_int(row.northern_combination),
            }
        )

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


async def get_olympics_dashboard(session: AsyncSession) -> OlympicsDashboardResponse:
    # ===== 1. Таблица по микрогруппам =====

    rows_stmt = select(
        OlympicsRow.microgroup,
        OlympicsRow.dept,
        OlympicsRow.team,
        OlympicsRow.figure_skating_count,
        OlympicsRow.curling_count,
        OlympicsRow.snowboard_money,
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
            snowboard=float(r.snowboard_money) if r.snowboard_money else None,
            hockey_ratio=float(r.hockey_ratio) if r.hockey_ratio else None,
        )
        for r in rows_result
    ]

    # ===== 2. Агрегация по отделам =====

    dept_stmt = select(
        OlympicsRow.dept,
        func.sum(OlympicsRow.figure_skating_count).label("figure_skating"),
        func.sum(OlympicsRow.curling_count).label("curling"),
        func.sum(OlympicsRow.snowboard_money).label("snowboard"),
        case(
            (
                func.sum(OlympicsRow.total_accounts) > 0,
                func.sum(OlympicsRow.bills_paid)
                / func.sum(OlympicsRow.total_accounts),
            ),
            else_=None,
        ).label("hockey_ratio"),
    ).group_by(OlympicsRow.dept)

    dept_result = (await session.execute(dept_stmt)).all()

    by_dept = [
        OlympicsDeptOut(
            dept=d.dept,
            figure_skating=d.figure_skating,
            curling=d.curling,
            snowboard=float(d.snowboard) if d.snowboard else None,
            hockey_ratio=float(d.hockey_ratio) if d.hockey_ratio else None,
        )
        for d in dept_result
    ]

    return OlympicsDashboardResponse(
        rows=rows,
        by_dept=by_dept,
    )