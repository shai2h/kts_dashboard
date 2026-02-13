from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_session
from .schemas import OlympicsIngestRequest, OlympicsRowIn
from .service import ingest_olympics_data

from .service import get_olympics_dashboard
from .schemas import OlympicsDashboardResponse

from typing import Union, List

router = APIRouter(
    prefix="/v1/olympics",
    tags=["olympics-dashboard"],
)


@router.post("/ingest")
async def ingest_olympics(
    payload: Union[OlympicsIngestRequest, List[OlympicsRowIn]],
    session: AsyncSession = Depends(get_session),
):
    if isinstance(payload, list):
        payload = OlympicsIngestRequest(rows=payload)
    return await ingest_olympics_data(session=session, payload=payload)


# @router.get("/dashboard", response_model=OlympicsDashboardResponse)
# async def olympics_dashboard(
#     session: AsyncSession = Depends(get_session),
# ):
#     return await get_olympics_dashboard(session)

@router.get("/dashboard", response_model=OlympicsDashboardResponse)
async def olympics_dashboard(session: AsyncSession = Depends(get_session)):
    data = await get_olympics_dashboard(session)
    print("=== HIT OLYMPICS DASHBOARD ROUTE (WITH BY_TEAM) ===", len(data.by_team))
    return data