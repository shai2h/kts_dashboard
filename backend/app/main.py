import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Убираем эту строку, если запускаем из корня проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.core.db import Base, engine
from app.modules.kts_dashboard.router import router as kts_router

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request

from fastapi.openapi.docs import get_swagger_ui_html


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

"""
Реализация шаблона
"""
templates = Jinja2Templates(directory="templates")


# если потом будут css/js файлы
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(kts_router, prefix="/api")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,  # type: ignore
        title=app.title + " - Swagger UI",  # type: ignore
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,  # type: ignore
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
