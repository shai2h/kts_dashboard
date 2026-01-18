# app/main.py
import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Убираем эту строку, если запускаем из корня проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.core.db import Base, engine
from app.modules.kts_dashboard.router import router as kts_router


# Проверка подключения к БД
print("DB_URL:", settings.DB_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Запуск приложения...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы созданы")
    yield
    await engine.dispose()
    print("Приложение остановлено")


# Создаём приложение после определения lifespan
app = FastAPI(description='KTS Dashboard', lifespan=lifespan)


# Подключаем роуты
app.include_router(kts_router, prefix="/api")



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
