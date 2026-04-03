import uuid
from datetime import datetime
from sqlalchemy import String, UUID, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from .database import Base

class FileMetadata(Base):
    __tablename__ = "files"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    original_name: Mapped[str] = mapped_column(String(255))
    storage_key: Mapped[str] = mapped_column(String(255), unique=True) # Назва файлу в MinIO
    size: Mapped[int] = mapped_column(BigInteger)
    content_type: Mapped[str] = mapped_column(String(100))
    uploader_id: Mapped[uuid.UUID] = mapped_column(UUID, index=True) # ID юзера з іншого сервісу
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())