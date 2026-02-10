from sqlalchemy import (
    Column,
    String,
    Integer,
    Numeric,
    DateTime,
    UniqueConstraint,
    Index,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
import uuid

from app.core.db import Base


class OlympicsRow(Base):
    """
    Одна строка = одна микрогруппа.
    Данные обновляются через UPSERT.
    """

    __tablename__ = "olympics_rows"

    id: Mapped[uuid.UUID] = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Организационные поля
    microgroup: Mapped[str] = Column(String, nullable=False)
    dept: Mapped[str] = Column(String, nullable=False)
    team: Mapped[str] = Column(String, nullable=False)

    # ===== Спортивные метрики =====

    # Фигурное катание — количество клиентов
    figure_skating_count: Mapped[int | None] = Column(Integer)

    # Кёрлинг — количество брендов
    curling_count: Mapped[int | None] = Column(Integer)

    # Сноуборд — поступление ДС
    snowboard_money: Mapped[float | None] = Column(Numeric(18, 2))

    # Хоккей — для расчёта конверсии
    total_accounts: Mapped[int | None] = Column(Integer)
    bills_paid: Mapped[int | None] = Column(Integer)

    # Биатлон — Интерколд + ПР
    biathlon_count: Mapped[int | None] = Column(Integer)

    # Фристайл — Rosso
    freestyle_count: Mapped[int | None] = Column(Integer)

    # Шорт-трек — итальянские бренды
    short_track_count: Mapped[int | None] = Column(Integer)

    # Ски-альпинизм — счета 100% оплачены и отгружены
    ski_alpenism_count: Mapped[int | None] = Column(Integer)

    # Конькобежный спорт — сумма 100% оплаченных и отгруженных
    speed_skating_money: Mapped[float | None] = Column(Numeric(18, 2))

    # Бобслей — сумма реализаций
    bobsleigh_money: Mapped[float | None] = Column(Numeric(18, 2))

    # Северная комбинация — частично оплачены или отгружены
    northern_combination_count: Mapped[int | None] = Column(Integer)

    # Техническое поле
    updated_at: Mapped[DateTime] = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        # Уникальность строки
        UniqueConstraint(
            "microgroup",
            "dept",
            "team",
            name="uq_olympics_row_microgroup",
        ),

        # Индексы под дашборды
        Index("ix_olympics_rows_dept", "dept"),
        Index("ix_olympics_rows_team", "team"),
    )

    def __repr__(self) -> str:
        return (
            f"<OlympicsRow "
            f"microgroup={self.microgroup!r} "
            f"dept={self.dept!r} "
            f"team={self.team!r}>"
        )
