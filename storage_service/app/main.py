import uuid
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_db, engine, Base
from . import schemas
from contextlib import asynccontextmanager
from .routes import upload, getfile
from .crud import MINIO_CLIENT, BUCKET_NAME

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 1. Створюємо таблиці в БД
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # 2. Перевіряємо та створюємо бакет у MinIO
    try:
        if not MINIO_CLIENT.bucket_exists(BUCKET_NAME):
            MINIO_CLIENT.make_bucket(BUCKET_NAME)
            print(f"✅ Бакет '{BUCKET_NAME}' створено успішно!")
        else:
            print(f"ℹ️ Бакет '{BUCKET_NAME}' вже існує.")
    except Exception as e:
        print(f"❌ Помилка MinIO при старті: {e}")
        
    yield

app = FastAPI(title="Storage Service", lifespan=lifespan)
app.include_router(upload.router)
app.include_router(getfile.router)