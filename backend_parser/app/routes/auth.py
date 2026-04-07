from fastapi import APIRouter, Request, Body
from ..services.proxy import base_proxy
from ..core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/{path:path}")
async def auth_proxy_post(path: str, request: Request, payload: dict = Body(None)):
    # Тепер сюди прилетить чисте "register"
    return await base_proxy(f"{settings.USER_SERVICE_URL}/{path}", request)

@router.get("/{path:path}")
async def auth_proxy_get(path: str, request: Request):
    return await base_proxy(f"{settings.USER_SERVICE_URL}/{path}", request)

@router.patch("/{path:path}")
async def auth_proxy_patch(path: str, request: Request, payload: dict = Body(None)):
    return await base_proxy(f"{settings.USER_SERVICE_URL}/{path}", request)

@router.delete("/{path:path}")
async def auth_proxy_delete(path: str, request: Request):
    return await base_proxy(f"{settings.USER_SERVICE_URL}/{path}", request)