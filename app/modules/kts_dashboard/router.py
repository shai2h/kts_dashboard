from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from modules.kts_dashboard.schemas import KtsDashboardItemIn
from app.core.db import get_session
from .models import KtsManagerPlan

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