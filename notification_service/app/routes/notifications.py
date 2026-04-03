from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from ..models import NotificationSetting, NotificationHistory
from ..schemas import NotificationCreate, SettingsUpdate
from ..services.email_service import send_email_task
from ..services.push_service import send_push_task
from uuid import UUID

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/send")
async def send_notification(
    data: NotificationCreate, 
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    # Шукаємо налаштування користувача
    result = await db.execute(select(NotificationSetting).where(NotificationSetting.user_id == data.user_id))
    settings = result.scalar_one_or_none()

    if not settings:
        return {"status": "ignored", "reason": "No settings for user"}

    # Логіка для ЧАТІВ (Тільки PUSH)
    if data.type == "chat":
        if settings.push_enabled and settings.push_token:
            background_tasks.add_task(send_push_task, settings.push_token, data.title, data.body)

    # Логіка для ЗАВДАНЬ та СИСТЕМНИХ (PUSH + EMAIL)
    else:
        if settings.push_enabled and settings.push_token:
            background_tasks.add_task(send_push_task, settings.push_token, data.title, data.body)
        
        if settings.email_enabled and settings.email:
            background_tasks.add_task(send_email_task, settings.email, data.title, data.body)

    # Зберігаємо в історію (опціонально)
    history = NotificationHistory(user_id=data.user_id, type=data.type, message=data.body, channel="mixed")
    db.add(history)
    await db.commit()

    return {"status": "processing"}

@router.put("/settings/{user_id}")
async def update_settings(user_id: UUID, update: SettingsUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(NotificationSetting).where(NotificationSetting.user_id == user_id))
    settings = result.scalar_one_or_none()

    if not settings:
        settings = NotificationSetting(user_id=user_id, **update.model_dump(exclude_none=True))
        db.add(settings)
    else:
        for key, value in update.model_dump(exclude_none=True).items():
            setattr(settings, key, value)

    await db.commit()
    return {"status": "updated"}