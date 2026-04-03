import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt
from sqlalchemy import select
import uvicorn
from .database import engine, Base, get_db
from .models import User
from .schemas import UserCreate, UserOut
from .routes import regisret, login, change_user_name, cnange_user_email

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏳ Спроба підключення до бази даних...")
    connected = False
    for i in range(10):  # 10 спроб
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("🚀 База готова, таблиці перевірено!")
            connected = True
            break
        except Exception as e:
            print(f"⚠️ Спроба {i+1}/10: База ще спить... ({e})")
            await asyncio.sleep(2)
    
    if not connected:
        print("❌ КРИТИЧНО: Не вдалося підключитися до бази!")
    yield

app = FastAPI(title="User Service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Цей блок виконується ПРИ СТАРТІ сервера
    async with engine.begin() as conn:
        # Створюємо всі таблиці, які описані в models.py
        await conn.run_sync(Base.metadata.create_all)
    print("🚀 Таблиці успішно створені або вже існують")
    yield
    # Тут можна додати дії при вимкненні (наприклад, закриття з'єднань)

# Передаємо lifespan у додаток
app = FastAPI(title="User Service", lifespan=lifespan)

app.include_router(regisret.router)
app.include_router(login.router)
app.include_router(change_user_name.router)
app.include_router(cnange_user_email.router)

