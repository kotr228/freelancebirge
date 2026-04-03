from fastapi import FastAPI
from .routes.tasks import router as task_router
from .database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Автоматичне створення таблиць при старті (зручно для розробки)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Task Manager Service", lifespan=lifespan)

app.include_router(task_router)

@app.get("/")
async def health_check():
    return {"status": "Task Manager is alive"}