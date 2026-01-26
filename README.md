## Технологии Backend

- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy (async)**
- **asyncpg**
- **Pydantic Settings**
- **Alembic**
- **Plotly**

## Технологии Frontend
- **Next.js**

## Требования к окружению

- **Docker** ≥ 20.10
- **Docker Compose** (плагин `docker-compose` или встроенный `docker compose`)


Проверка:
```bash
docker --version
docker compose version

## Запуск проекта

# 1. Скопируй .env и создай .env.local для фронта
cp .env_example .env
echo "NEXT_PUBLIC_API_URL=http://127.0.0.1:8000" > frontend/dashboard/.env.local

# 2. Собери образы
docker compose build

# 3. Запусти контейнеры в фоне
docker compose up -d

# 4. Применить миграции (если не запускаются автоматически)
docker compose exec backend alembic upgrade head