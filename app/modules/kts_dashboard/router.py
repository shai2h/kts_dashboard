from fastapi import APIRouter
from typing import List
from modules.kts_dashboard.schemas import KtsDashboardItemIn


router = APIRouter()

@router.post("/items")
async def upload_items(items: list[KtsDashboardItemIn]):
    total_plan = sum(i.plan for i in items)
    return {"count": len(items), "total_plan": str(total_plan)}

