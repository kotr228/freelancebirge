import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://admin:mongo_password@chat_mongodb:27017")

client = AsyncIOMotorClient(MONGO_URL)
db = client["chat_db"]
# Колекція повідомлень
messages_collection = db["messages"]