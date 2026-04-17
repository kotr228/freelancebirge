from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from ..database import get_db
from ..models import Task, TaskStatus
from ..schemas import TaskCreate, TaskResponse
from uuid import UUID
from typing import List

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Створити нову задачу
@router.post("/", response_model=TaskResponse)
async def create_task(task_in: TaskCreate, employer_id: UUID, db: AsyncSession = Depends(get_db)):
    new_task = Task(**task_in.model_dump(), employer_id=employer_id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

# Взяти задачу фрілансером
@router.patch("/{task_id}/take")
async def take_task(task_id: UUID, freelancer_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status != TaskStatus.OPEN:
        raise HTTPException(status_code=400, detail="Task is not open for taking")
    if task.employer_id == freelancer_id:
        raise HTTPException(status_code=400, detail="You cannot work on your own task")

    task.freelancer_id = freelancer_id
    task.status = TaskStatus.IN_PROGRESS
    await db.commit()
    return {"status": "success", "message": "Task taken in progress"}

# Отримати всі задачі користувача (і де він бос, і де він робітник)
@router.get("/my-tasks/{user_id}", response_model=List[TaskResponse])
async def get_user_tasks(user_id: UUID, db: AsyncSession = Depends(get_db)):
    query = select(Task).where(or_(Task.employer_id == user_id, Task.freelancer_id == user_id))
    result = await db.execute(query)
    return result.scalars().all()

@router.delete("/{task_id}")
async def delete_task(task_id: UUID, employer_id: UUID, db: AsyncSession = Depends(get_db)):
    # Шукаємо задачу
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    # Перевіряємо, чи має право цей юзер видаляти задачу
    if task.employer_id != employer_id:
        raise HTTPException(status_code=403, detail="Only the employer can delete this task")
        
    # Видаляємо
    await db.delete(task)
    await db.commit()
    return {"status": "success", "message": "Task deleted"}