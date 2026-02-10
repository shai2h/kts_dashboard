from pydantic import BaseModel, Field
from typing import List, Optional


# Входящая строка (как приходит из JSON)

class OlympicsRowIn(BaseModel):
    microgroup: str = Field(..., description="Микрогруппа")
    dept: str = Field(..., description="Отдел")
    team: str = Field(..., description="Команда")

    # Метрики (все приходят строками, парсятся в сервисе)
    figure_skating: Optional[str] = None
    curling: Optional[str] = None
    snowboard: Optional[str] = None

    total_accounts: Optional[str] = None
    bills_paid: Optional[str] = None

    biathlon: Optional[str] = None
    freestyle: Optional[str] = None
    short_track: Optional[str] = None
    ski_alpenism: Optional[str] = None

    speed_skating: Optional[str] = None
    bobsleigh: Optional[str] = None
    northern_combination: Optional[str] = None


class OlympicsIngestRequest(BaseModel):
    rows: List[OlympicsRowIn]


class OlympicsIngestResponse(BaseModel):
    rows_received: int
    rows_processed: int


class OlympicsRowOut(BaseModel):
    microgroup: str
    dept: str
    team: str

    figure_skating: Optional[int]
    curling: Optional[int]
    snowboard: Optional[float]

    hockey_ratio: Optional[float]


class OlympicsDeptOut(BaseModel):
    dept: str

    figure_skating: Optional[int]
    curling: Optional[int]
    snowboard: Optional[float]

    hockey_ratio: Optional[float]


class OlympicsDashboardResponse(BaseModel):
    rows: List[OlympicsRowOut]
    by_dept: List[OlympicsDeptOut]