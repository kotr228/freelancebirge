import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# ВАЖЛИВО: Беремо URL з Docker Compose, якщо його немає - ставимо локальний
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user_admin:secret_password@localhost:5432/user_db")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with async_session() as session:
        yield session