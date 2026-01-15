from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from core.config import settings
from sqlalchemy.orm import DeclarativeBase


engine = create_async_engine(settings.DB_URL) # можно использовать echo=True для небольшого логирования

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass