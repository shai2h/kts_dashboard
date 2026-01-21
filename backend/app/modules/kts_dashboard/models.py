from sqlalchemy import Column, Integer, String, Numeric
from app.core.db import Base


class KtsManagerPlan(Base):
    __tablename__ = "kts_manager_plan"

    id = Column(Integer, primary_key=True)
    manager = Column(String, nullable=False)
    podr = Column(String, nullable=False)
    plan = Column(Numeric(18, 2), nullable=False)
    tec = Column(Numeric(18, 2), nullable=True)
    procent = Column(Numeric(10, 2), nullable=False)