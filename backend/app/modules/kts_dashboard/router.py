from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, func

from modules.kts_dashboard.schemas import KtsDashboardItemIn
from app.core.db import get_session
from .models import KtsManagerPlan

from fastapi.templating import Jinja2Templates

import random

# Список цитат — можно расширять
QUOTES = [
"«Каждый звонок — это шаг к цели. Ни один не бывает напрасным»",
"«Продажи — это не «впаривание». Это помощь клиенту принять правильное решение»",
"«Успех продавца — это 80% настойчивости и 20% удачи»",
"«Не говори «мне повезёт». Говори «я готов, и я сделаю это»»",
"«Самый ценный клиент сегодня — тот, кто сказал «нет» вчера»",
"«Ваш комфорт — главный враг вашего роста. Звоните тому, кто пугает»",
"«Не считайте дни. Дни должны считать вас»",
"«Десять отказов — это цена одной победы. Продолжайте»",
"«Продажи создают не красивые презентации, а правильные вопросы»",
"«Ваш план на день важнее, чем ваш талант. Следуйте ему»",
"«Продажи — это не спринт, а марафон. Постоянство побеждает талант»",
"«Цена сомнения — упущенная сделка. Верьте в свой продукт»",
"«Ваш следующий большой клиент ждет вашего звонка прямо сейчас»",
"«Никто не просыпается с желанием купить. Но все просыпаются с желанием решить свою проблему»",
"«Сфокусируйтесь не на квоте, а на процессе. Квота придет сама»",
"«Самый важный разговор — тот, который вы боитесь начать»",
"«Успех — это когда подготовка встречается с возможностью. Готовьте скрипты»",
"«Не продавайте продукт. Продавайте лучшее будущее для вашего клиента»",
"«Если вы не звоните, ваш конкурент уже набирает номер»",
"«Запомните: каждый «нет» приближает вас к «да»»"
]

templates = Jinja2Templates(directory="templates")

def rub(value: float | int | None) -> str:
    if value is None:
        return "—"
    try:
        return f"{int(value):,}".replace(",", " ") + " ₽"
    except (ValueError, TypeError):
        return str(value)


templates.env.filters["rub"] = rub

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

    # Рандомные цитатки на вывод к дашборду
    quote = random.choice(QUOTES)

    context = {
        "request": request,
        "total_plan": float(total_plan or 0),
        "total_tec": float(total_tec or 0),
        "total_percent": total_percent,
        "by_podr": by_podr,
        "managers_by_podr": managers_by_podr,
        "quote": quote, # цитатки
    }
    return templates.TemplateResponse("dashboard.html", context)