from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from datetime import timedelta

from ..database import get_db
from ..models import User
# Імпортуємо наші функції безпеки з auth.py
from ..auth import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

# Створюємо схеми спеціально для логіну та відповіді
class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token, tags=["users"], summary="User login")
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    try:
        # 1. Шукаємо користувача в базі
        query = select(User).where(User.username == user_data.username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        
        # 2. Перевіряємо, чи існує юзер і чи збігається пароль
        if not user or not verify_password(user_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Неправильний логін або пароль")

        # 3. Генеруємо JWT токен
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        # У токен зашиваємо ID користувача (sub), щоб Парсер знав, хто це
        access_token = create_access_token(
            data={"sub": str(user.id)}, 
            expires_delta=access_token_expires
        )

        # 4. Повертаємо токен
        return {"access_token": access_token, "token_type": "bearer"}

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ СПРАВЖНЯ ПОМИЛКА ЛОГІНУ: {e}")
        raise HTTPException(status_code=500, detail="Внутрішня помилка сервера")