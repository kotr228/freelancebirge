from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, tasks, storage, notify, chat

app = FastAPI(title="FreelanceBirge Central Gateway", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Підключаємо всі наші модулі
app.include_router(auth.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(storage.router, prefix="/api/v1")
app.include_router(notify.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")

@app.get("/health", tags=["System"])
async def health():
    return {"status": "Parser is healthy", "modules": 5}