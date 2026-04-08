from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from ..models import User
from ..schemas import UserCreate, UserOut
# Імпортуємо функцію хешування з auth.py
from ..auth import hash_password

router = APIRouter()

@router.post("/register", response_model=UserOut, tags=["users"], summary="User registration")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Перевірка, чи існує вже такий користувач
        query = select(User).where(User.username == user_data.username)
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Користувач з таким іменем вже існує")

        # Використовуємо імпортовану функцію
        hashed_pwd = hash_password(user_data.password)

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_pwd
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ СПРАВЖНЯ ПОМИЛКА РЕЄСТРАЦІЇ: {e}")
        raise HTTPException(status_code=500, detail="Помилка при створенні користувача")