from fastapi import FastAPI
from .routes.chat import router as chat_router

app = FastAPI(title="Chat Service")

app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "Chat Microservice is running"}