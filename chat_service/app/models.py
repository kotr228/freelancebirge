from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Attachment(BaseModel):
    file_id: UUID
    file_name: str
    file_type: str  # image, document, video, etc.
    url: Optional[str] = None # Буде заповнюватися парсером через storage_service

class MessageCreate(BaseModel):
    text: Optional[str] = None
    attachments: List[Attachment] = []

class MessageDocument(MessageCreate):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    sender_id: UUID
    room_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True