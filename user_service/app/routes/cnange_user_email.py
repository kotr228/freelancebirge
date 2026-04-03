from fastapi import APIRouter, FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import bcrypt
from sqlalchemy import select
import uvicorn
from ..database import engine, Base, get_db
from ..models import User
from ..schemas import UserCreate, UserOut
import uuid

router = APIRouter()

@router.put("/change-email", response_model=UserOut, tags=["users"], summary="Change user email", description="This endpoint allows users to change their email.")
async def change_user_email(user_id: uuid.UUID, new_email: str, db: AsyncSession = Depends(get_db)):
    try:
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if the new email is already taken
        query = select(User).where(User.email == new_email)
        result = await db.execute(query)
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already taken")
        
        user.email = new_email
        await db.commit()
        await db.refresh(user)
        return user

    except Exception as e:
        print(f"❌ ПРАВЖНЯ ПОМИЛКА: {e}")
        raise HTTPException(status_code=500, detail="Помилка при зміні електронної пошти користувача")