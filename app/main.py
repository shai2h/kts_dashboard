from fastapi import FastAPI
import sys
import os
import uvicorn
# Добавляем корень проекта в путь, чтобы можно было импортировать "app"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.modules.kts_dashboard.router import router as kts_router


app = FastAPI(description='KTS Dashboard')


app.include_router(kts_router, prefix="/api")


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )