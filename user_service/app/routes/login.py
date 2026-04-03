from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt
from sqlalchemy import select
import uvicorn
from ..database import engine, Base, get_db
from ..models import User
from ..schemas import UserCreate, UserOut

router = APIRouter()

def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

@router.post("/login", response_model=UserOut, tags=["users"], summary="User login", description="This endpoint allows users to log in.")
async def login(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        query = select(User).where(User.username == user_data.username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=400, detail="Invalid username or password")

        # Перевірка пароля
        if not bcrypt.checkpw(user_data.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            raise HTTPException(status_code=400, detail="Invalid username or password")

        return user

    except Exception as e:
        print(f"❌ ПРАВЖНЯ ПОМИЛКА: {e}")
        raise HTTPException(status_code=500, detail="Помилка при вході користувача")