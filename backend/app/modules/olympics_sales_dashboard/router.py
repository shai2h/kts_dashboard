from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from .schemas import OlympicsIngestRequest
from .service import ingest_olympics_data

from .service import get_olympics_dashboard
from .schemas import OlympicsDashboardResponse

router = APIRouter(
    prefix="/v1/olympics",
    tags=["olympics-dashboard"],
)


@router.post("/ingest")
async def ingest_olympics(
    payload: OlympicsIngestRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Загрузка данных олимпиады.
    Повторная загрузка обновляет существующие строки (UPSERT).
    """
    return await ingest_olympics_data(session=session, payload=payload)


@router.get("/dashboard", response_model=OlympicsDashboardResponse)
async def olympics_dashboard(
    session: AsyncSession = Depends(get_session),
):
    return await get_olympics_dashboard(session)