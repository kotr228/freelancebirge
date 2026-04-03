import uuid
import io
import os
from sqlalchemy.ext.asyncio import AsyncSession
from .models import FileMetadata
from minio import Minio

# Налаштування MinIO
MINIO_CLIENT = Minio(
    os.getenv("MINIO_ENDPOINT", "minio_storage:9000"),
    access_key=os.getenv("MINIO_ROOT_USER", "admin"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD", "password123"),
    secure=False
)
BUCKET_NAME = "media"

async def upload_file_to_storage(
    db: AsyncSession, 
    file_data: bytes, 
    filename: str, 
    content_type: str, 
    uploader_id: uuid.UUID
):
    # 1. Генеруємо ключ для MinIO
    storage_key = f"{uuid.uuid4()}_{filename}"

    # 2. Шлемо в MinIO
    MINIO_CLIENT.put_object(
        BUCKET_NAME,
        storage_key,
        io.BytesIO(file_data),
        length=len(file_data),
        content_type=content_type
    )

    # 3. Записуємо метадані в базу
    db_file = FileMetadata(
        original_name=filename,
        storage_key=storage_key,
        size=len(file_data),
        content_type=content_type,
        uploader_id=uploader_id
    )
    
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)
    return db_file