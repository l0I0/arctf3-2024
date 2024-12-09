from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from environs import Env

env = Env()
POSTGRES_URL_ASYNC = env("POSTGRES_URL_ASYNC")

engine = create_async_engine(POSTGRES_URL_ASYNC, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Создаем Base без автоматического создания таблиц
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close() 