## Технологии

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy (async)**
- **asyncpg**
- **Pydantic Settings**
- **Alembic**
- **Plotly**

## Запуск проекта

```bash
# 1. Скопируй .env
cp env_example .env

# 2. Установи зависимости
pip install -r requirements.txt

# 3. Запусти приложение
uvicorn app.main:app --reload 'OR' python main.py