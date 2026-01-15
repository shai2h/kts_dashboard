app/
  main.py
  core/
    config.py        # настройки (Pydantic Settings, .env)
    db.py            # async engine + session (SQLAlchemy, asyncpg)
  modules/
    kts_dashboard/
      router.py      # HTTP ручки
      schemas.py     # Pydantic-модели
      models.py      # SQLAlchemy ORM модели
      repository.py  # работа с БД
      service.py     # бизнес-логика
  migrations/        # Alembic
.env