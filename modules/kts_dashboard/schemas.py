from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal


class KtsDashboardItemIn(BaseModel):
    manager: str
    plan: str
    tec: Optional[str] = ""
    procent: str
    podr: str

    @field_validator("plan", "tec", "procent", mode="before")
    @classmethod
    def parse_ru_number(cls, v: str | None):
        # ожидаем строку формата "14 109 923,7" или ""
        if v is None or v == "":
            return None
        cleaned = v.replace("\u00A0", " ").replace(" ", "").replace(",", ".")
        return Decimal(cleaned)