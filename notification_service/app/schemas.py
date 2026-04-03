from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from typing import Optional, List

class NotificationCreate(BaseModel):
    user_id: UUID
    type: str # chat, task, system
    title: str
    body: str

class SettingsUpdate(BaseModel):
    email: Optional[str] = None
    push_token: Optional[str] = None
    email_enabled: Optional[bool] = None
    push_enabled: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)