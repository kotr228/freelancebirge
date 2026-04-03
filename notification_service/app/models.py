import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class NotificationSetting(Base):
    __tablename__ = "notification_settings"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)
    push_token: Mapped[str] = mapped_column(String(500), nullable=True) # Токен для мобільного додатка
    email_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    push_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

class NotificationHistory(Base):
    __tablename__ = "notification_history"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    type: Mapped[str] = mapped_column(String(50)) # chat, task, system
    message: Mapped[str] = mapped_column(String(1000))
    channel: Mapped[str] = mapped_column(String(20)) # email, push
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)