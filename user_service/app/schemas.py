from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime

# Що ми очікуємо від клієнта при реєстрації
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)

# Що ми віддаємо клієнту (без пароля!)
class UserOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class PhotoCreate(BaseModel):
    url: str  # Тут буде посилання від іншого сервісу
    is_avatar: bool = False

class PhotoOut(BaseModel):
    id: UUID
    url: str
    is_avatar: bool
    created_at: datetime

    class Config:
        from_attributes = True