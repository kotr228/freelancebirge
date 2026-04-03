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

@router.post("/register", response_model=UserOut, tags=["users"], summary="User registration", description="This endpoint allows users to register.")
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        query = select(User).where(User.username == user_data.username)
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already taken")

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

    except Exception as e:
        print(f"❌ ПРАВЖНЯ ПОМИЛКА: {e}")
        raise HTTPException(status_code=500, detail="Помилка при створенні користувача")