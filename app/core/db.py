from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
import os
from core.config import settings

DATABASE_URL = settings.DB_URL


# Создаём асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)


# Фабрика асинхронных сессий
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


# Базовый класс для моделей
Base = declarative_base()


# Правильно типизированная зависимость
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session