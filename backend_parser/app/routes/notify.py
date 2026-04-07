from fastapi import APIRouter, Request, Body
from ..services.proxy import base_proxy
from ..core.config import settings

router = APIRouter(prefix="/notify", tags=["Notify"])

@router.post("/{path:path}")
async def proxy_post(path: str, request: Request, payload: dict = Body(None)):
    return await base_proxy(f"{settings.NOTIFY_SERVICE_URL}/notifications/{path}", request)

@router.get("/{path:path}")
async def proxy_get(path: str, request: Request):
    return await base_proxy(f"{settings.NOTIFY_SERVICE_URL}/notifications/{path}", request)

@router.patch("/{path:path}")
async def proxy_patch(path: str, request: Request, payload: dict = Body(None)):
    return await base_proxy(f"{settings.NOTIFY_SERVICE_URL}/notifications/{path}", request)

@router.delete("/{path:path}")
async def proxy_delete(path: str, request: Request):
    return await base_proxy(f"{settings.NOTIFY_SERVICE_URL}/notifications/{path}", request)