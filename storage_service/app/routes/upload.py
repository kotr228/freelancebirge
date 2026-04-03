import uuid
from fastapi import APIRouter, FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db, engine, Base
from .. import crud, schemas
from contextlib import asynccontextmanager

router = APIRouter()

@router.post("/upload", response_model=schemas.FileResponse)
async def test_upload(
    file: UploadFile = File(...), 
    db: AsyncSession = Depends(get_db)
):
    # Поки що ID завантажувача фейковий (потім буде з токена)
    test_uploader_id = uuid.uuid4()
    
    try:
        content = await file.read()
        db_record = await crud.upload_file_to_storage(
            db=db,
            file_data=content,
            filename=file.filename,
            content_type=file.content_type,
            uploader_id=test_uploader_id
        )
        
        # Формуємо URL для відповіді
        file_url = f"http://localhost:9000/media/{db_record.storage_key}"
        
        return {
            "id": db_record.id,
            "url": file_url,
            "original_name": db_record.original_name,
            "content_type": db_record.content_type,
            "size": db_record.size
        }
    except Exception as e:
        print(f"❌ Помилка: {e}")
        raise HTTPException(status_code=500, detail="Не вдалося завантажити файл")