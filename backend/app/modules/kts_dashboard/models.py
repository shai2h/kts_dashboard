from sqlalchemy import Column, Integer, String, Numeric
from app.core.db import Base
from sqlalchemy import UniqueConstraint

class KtsManagerPlan(Base):
    __tablename__ = "kts_manager_plan"

    id = Column(Integer, primary_key=True)
    manager = Column(String, nullable=False)
    podr = Column(String, nullable=False)

    plan = Column(Numeric)
    tec = Column(Numeric)
    procent = Column(Numeric)

    __table_args__ = (
        UniqueConstraint("manager", "podr", name="uq_manager_podr"),
    )
