from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class OlympicsRowIn(BaseModel):
    model_config = ConfigDict(extra="ignore")  # хоккей можно игнорить

    microgroup: str = Field(...)
    dept: str = Field(...)
    team: str = Field(...)

    rop: str = Field(...)

    figure_skating: Optional[int] = None
    curling: Optional[int] = None
    snowboard: Optional[float] = None

    total_accounts: Optional[int] = None
    bills_paid: Optional[int] = None

    biathlon: Optional[int] = None
    freestyle: Optional[int] = None
    short_track: Optional[int] = None
    ski_alpenism: Optional[int] = None

    speed_skating: Optional[float] = None
    bobsleigh: Optional[float] = None
    northern_combination: Optional[int] = None


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

    biathlon: Optional[int]
    freestyle: Optional[int]
    short_track: Optional[int]
    ski_alpenism: Optional[int]

    speed_skating: Optional[float]
    bobsleigh: Optional[float]

    northern_combination: Optional[int]

    hockey_ratio: Optional[float]


class OlympicsDeptOut(BaseModel):
    dept: str

    figure_skating: Optional[int]
    curling: Optional[int]
    snowboard: Optional[float]

    biathlon: Optional[int]
    freestyle: Optional[int]
    short_track: Optional[int]
    ski_alpenism: Optional[int]

    speed_skating: Optional[float]
    bobsleigh: Optional[float]

    northern_combination: Optional[int]

    total_accounts: int = 0
    bills_paid: int = 0
    hockey_ratio: Optional[float] = None


class OlympicsTeamOut(BaseModel):
    team: str

    figure_skating: Optional[int] = None
    curling: Optional[int] = None
    snowboard: Optional[float] = None

    biathlon: Optional[int] = None
    freestyle: Optional[int] = None
    short_track: Optional[int] = None
    ski_alpenism: Optional[int] = None
    speed_skating: Optional[float] = None
    bobsleigh: Optional[float] = None
    northern_combination: Optional[int] = None

    total_accounts: int = 0
    bills_paid: int = 0
    hockey_ratio: Optional[float] = None


class OlympicsDashboardResponse(BaseModel):
    rows: List[OlympicsRowOut]
    by_dept: List[OlympicsDeptOut]
    by_team: List[OlympicsTeamOut]