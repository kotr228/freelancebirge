import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import String, DateTime, Numeric, Enum as SqlEnum, UUID
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String(2000), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    # ID користувачів з нашого user_service
    employer_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    freelancer_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=True)
    
    status: Mapped[TaskStatus] = mapped_column(SqlEnum(TaskStatus), default=TaskStatus.OPEN)
    
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)