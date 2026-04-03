from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional
from .models import TaskStatus

class TaskBase(BaseModel):
    title: str
    description: str
    price: float
    deadline: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: UUID
    employer_id: UUID
    freelancer_id: Optional[UUID]
    status: TaskStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)