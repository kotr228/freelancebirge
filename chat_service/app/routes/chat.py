import json
from bson import ObjectId # <--- ДОДАЙ ЦЕЙ ІМПОРТ ЗВЕРХУ
from pydantic.deprecated.json import pydantic_encoder
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from ..database import messages_collection
from ..models import MessageCreate, MessageDocument
from ..utils.manager import manager
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["Chat"])

# 1. Відправка повідомлення (REST)
@router.post("/{room_id}/send")
async def send_message(room_id: str, user_id: str, msg: MessageCreate):
    # Формуємо документ для MongoDB
    message_dict = msg.dict()
    message_dict.update({
        "sender_id": user_id,
        "room_id": room_id,
        "timestamp": datetime.utcnow()
    })
    
    # Зберігаємо в базу
    result = await messages_collection.insert_one(message_dict)
    message_dict["id"] = str(result.inserted_id)
    
    # OBSERVER: Розсилаємо через WebSocket
    # Парсер отримає цей JSON і віддасть на UI
    await manager.broadcast(room_id, {
        "type": "new_message",
        "data": json_compatible(message_dict)
    })
    
    return {"status": "sent", "message_id": str(result.inserted_id)}

# 2. Отримання історії
@router.get("/{room_id}/history")
async def get_history(room_id: str, limit: int = 50):
    cursor = messages_collection.find({"room_id": room_id}).sort("timestamp", -1).limit(limit)
    messages = await cursor.to_list(length=limit)
    
    for m in messages:
        m["id"] = str(m.pop("_id"))
    return messages

# 3. WebSocket (Observer Interface)
@router.websocket("/ws/{room_id}/{user_id}")
async def chat_websocket(websocket: WebSocket, room_id: str, user_id: str):
    await manager.connect(websocket, room_id, user_id)
    try:
        while True:
            # Чекаємо пінгів або системних івентів
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(room_id, user_id)

def json_compatible(data):
    # Створюємо власного перекладача для JSON
    def custom_encoder(obj):
        if isinstance(obj, ObjectId):
            return str(obj) # Якщо це ObjectId з Монго, робимо з нього звичайний рядок
        return pydantic_encoder(obj) # Для всього іншого використовуємо стандартний Pydantic

    return json.loads(json.dumps(data, default=custom_encoder))