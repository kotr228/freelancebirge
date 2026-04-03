from fastapi import FastAPI
from .routes.notifications import router as notify_router
from .database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Notification Service", lifespan=lifespan)
app.include_router(notify_router)