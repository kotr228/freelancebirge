import uuid
from fastapi import APIRouter, FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db, engine, Base
from .. import crud, schemas
from contextlib import asynccontextmanager

router = APIRouter()

@router.get("/getfile/{file_id}", response_model=schemas.FileResponse)
async def get_file(file_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    try:
        file_record = await crud.get_file_by_id(db, file_id)
        
        if not file_record:
            raise HTTPException(status_code=404, detail="File not found")
        
        file_url = f"http://localhost:9000/media/{file_record.storage_key}"
        
        return {
            "id": file_record.id,
            "url": file_url,
            "original_name": file_record.original_name,
            "content_type": file_record.content_type,
            "size": file_record.size
        }
    except Exception as e:
        print(f"❌ Помилка: {e}")
        raise HTTPException(status_code=500, detail="Не вдалося отримати файл")