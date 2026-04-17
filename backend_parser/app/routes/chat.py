import asyncio
import websockets
from fastapi import APIRouter, Request, Body, WebSocket, WebSocketDisconnect
from ..services.proxy import base_proxy
from ..core.config import settings

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/{path:path}")
async def proxy_post(path: str, request: Request, payload: dict = Body(None)):
    # ДОДАЛИ /chat/ ПЕРЕД {path}
    return await base_proxy(f"{settings.CHAT_SERVICE_URL}/chat/{path}", request)

@router.get("/{path:path}")
async def proxy_get(path: str, request: Request):
    return await base_proxy(f"{settings.CHAT_SERVICE_URL}/chat/{path}", request)

@router.patch("/{path:path}")
async def proxy_patch(path: str, request: Request, payload: dict = Body(None)):
    return await base_proxy(f"{settings.CHAT_SERVICE_URL}/chat/{path}", request)

@router.delete("/{path:path}")
async def proxy_delete(path: str, request: Request):
    return await base_proxy(f"{settings.CHAT_SERVICE_URL}/chat/{path}", request)

@router.websocket("/ws/{room_id}/{user_id}")
async def websocket_proxy(websocket: WebSocket, room_id: str, user_id: str):
    await websocket.accept()
    
    backend_ws_url = f"ws://chat_service:8000/chat/ws/{room_id}/{user_id}"

    try:
        async with websockets.connect(backend_ws_url) as backend_ws:
            
            async def forward_to_backend():
                try:
                    while True:
                        data = await websocket.receive_text()
                        await backend_ws.send(data)
                except WebSocketDisconnect:
                    pass

            async def forward_to_client():
                try:
                    while True:
                        data = await backend_ws.recv()
                        await websocket.send_text(data)
                except websockets.exceptions.ConnectionClosed:
                    pass

            await asyncio.gather(
                forward_to_backend(),
                forward_to_client()
            )
            
    except Exception as e:
        print(f"WebSocket Proxy Error: {e}")
        if not websocket.client_state.name == "DISCONNECTED":
            await websocket.close(code=1011)