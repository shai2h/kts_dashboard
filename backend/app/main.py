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

from fastapi.openapi.docs import get_swagger_ui_html

from fastapi.middleware.cors import CORSMiddleware


# Проверка подключения к БД
print("DB_URL:", settings.ASYNC_DB_URL)


# Создаём приложение после определения lifespan
app = FastAPI(description='KTS Dashboard')


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Или ["*"] для всех (не для продакшена)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"status": "ok"}



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
