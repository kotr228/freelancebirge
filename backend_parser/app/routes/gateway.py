from fastapi import APIRouter, HTTPException, Request, Response
import httpx
from ..core.config import settings
from ..services.aggregator import aggregator

router = APIRouter()

# Універсальний проксі для User Service
@router.api_route("/auth/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_auth(path: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{settings.USER_SERVICE_URL}/{path}"
        content = await request.body()
        res = await client.request(
            method=request.method,
            url=url,
            content=content,
            headers=dict(request.headers),
            params=dict(request.query_params)
        )
        return Response(content=res.content, status_code=res.status_code, headers=dict(res.headers))

# Агрегований ендпоінт для задач (використовує наш Aggregator)
@router.get("/feed/tasks/{task_id}")
async def get_task_full(task_id: str):
    data = await aggregator.get_full_task_details(task_id)
    if not data:
        raise HTTPException(status_code=404, detail="Task details not found")
    return data

# Проксі для сповіщень
@router.post("/push/settings/{user_id}")
async def update_notify_settings(user_id: str, request: Request):
    async with httpx.AsyncClient() as client:
        url = f"{settings.NOTIFY_SERVICE_URL}/notifications/settings/{user_id}"
        res = await client.put(url, json=await request.json())
        return Response(content=res.content, status_code=res.status_code)