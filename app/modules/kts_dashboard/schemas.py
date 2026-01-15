from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal

class KtsDashboardItemIn(BaseModel):
    manager: str
    plan: Decimal       # наружу уже как число
    tec: Optional[Decimal] = None
    procent: Decimal
    podr: str

    @field_validator("plan", "tec", "procent", mode="before")
    @classmethod
    def parse_ru_number(cls, v):
        # ожидаем "27 000 121" или "14 109 923,7" или ""/None
        if v is None or v == "":
            return None
        if isinstance(v, (int, float, Decimal)):
            return v
        s = str(v)
        s = s.replace("\u00A0", " ")  # неразрывные пробелы
        s = s.replace(" ", "")        # убираем пробелы
        s = s.replace(",", ".")       # заменяем запятую на точку
        return Decimal(s)