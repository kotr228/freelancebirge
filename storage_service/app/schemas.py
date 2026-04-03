from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class FileResponse(BaseModel):
    id: UUID
    url: str
    original_name: str
    content_type: str
    size: int

    class Config:
        from_attributes = True