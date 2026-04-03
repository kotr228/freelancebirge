from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Optional

class MessageRead(BaseModel):
    room_id: str
    sender_id: UUID
    text: str
    file_ids: List[UUID]
    timestamp: datetime

    class Config:
        from_attributes = True # Для Pydantic v2