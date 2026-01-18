from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, func

from modules.kts_dashboard.schemas import KtsDashboardItemIn
from app.core.db import get_session
from .models import KtsManagerPlan

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.post("/items")
async def upload_items(
    items: list[KtsDashboardItemIn],
    session: AsyncSession = Depends(get_session),
):
    # считаем сумму для ответа
    total_plan = sum(i.plan for i in items)

    # готовим список словарей для вставки
    values = [
        {
            "manager": i.manager,
            "podr": i.podr,
            "plan": i.plan,
            "tec": i.tec,
            "procent": i.procent,
        }
        for i in items
    ]

    stmt = insert(KtsManagerPlan).values(values)
    await session.execute(stmt)
    await session.commit()

    return {"count": len(items), "total_plan": str(total_plan)}


# Роутер для дашборда
@router.get("/dashboard")
async def dashboard(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    # 1. Общий план и факт
    total = await session.execute(
        select(
            func.coalesce(func.sum(KtsManagerPlan.plan), 0),
            func.coalesce(func.sum(KtsManagerPlan.tec), 0),
        )
    )
    total_plan, total_tec = total.one()
    total_percent = float(total_tec / total_plan * 100) if total_plan else 0.0

    # 2. План/факт по направлениям (podr)
    by_podr_result = await session.execute(
        select(
            KtsManagerPlan.podr,
            func.coalesce(func.sum(KtsManagerPlan.plan), 0),
            func.coalesce(func.sum(KtsManagerPlan.tec), 0),
        ).group_by(KtsManagerPlan.podr)
    )
    by_podr_rows = by_podr_result.all()

    by_podr = []
    for podr, plan_sum, tec_sum in by_podr_rows:
        percent = float(tec_sum / plan_sum * 100) if plan_sum else 0.0
        by_podr.append(
            {
                "podr": podr,
                "plan": float(plan_sum or 0),
                "tec": float(tec_sum or 0),
                "percent": percent,
            }
        )

    # 3. Менеджеры по каждому направлению
    managers_result = await session.execute(
        select(
            KtsManagerPlan.podr,
            KtsManagerPlan.manager,
            KtsManagerPlan.plan,
            KtsManagerPlan.tec,
            KtsManagerPlan.procent,
        ).order_by(KtsManagerPlan.podr, KtsManagerPlan.manager)
    )
    manager_rows = managers_result.all()

    managers_by_podr: dict[str, list[dict]] = {}
    for podr, manager, plan, tec, procent in manager_rows:
        managers_by_podr.setdefault(podr, []).append(
            {
                "manager": manager,
                "plan": float(plan or 0),
                "tec": float(tec or 0),
                "percent": float(procent or 0),
            }
        )

    context = {
        "request": request,
        "total_plan": float(total_plan or 0),
        "total_tec": float(total_tec or 0),
        "total_percent": total_percent,
        "by_podr": by_podr,
        "managers_by_podr": managers_by_podr,
    }
    return templates.TemplateResponse("dashboard.html", context)