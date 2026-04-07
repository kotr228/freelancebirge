from fastapi import APIRouter, Request, Body, Depends
from ..services.proxy import base_proxy
from ..core.config import settings
from ..core.security import verify_jwt_token

router = APIRouter(prefix="/tasks", tags=["Tasks"], dependencies=[Depends(verify_jwt_token)])

@router.post("/{path:path}")
async def proxy_post(path: str, request: Request, payload: dict = Body(None), user_id: str = Depends(verify_jwt_token)):
    return await base_proxy(f"{settings.TASK_SERVICE_URL}/tasks/{path}", request, user_id)

@router.get("/{path:path}")
async def proxy_get(path: str, request: Request, user_id: str = Depends(verify_jwt_token)):
    return await base_proxy(f"{settings.TASK_SERVICE_URL}/tasks/{path}", request, user_id)

@router.patch("/{path:path}")
async def proxy_patch(path: str, request: Request, payload: dict = Body(None), user_id: str = Depends(verify_jwt_token)):
    return await base_proxy(f"{settings.TASK_SERVICE_URL}/tasks/{path}", request, user_id)

@router.delete("/{path:path}")
async def proxy_delete(path: str, request: Request, user_id: str = Depends(verify_jwt_token)):
    return await base_proxy(f"{settings.TASK_SERVICE_URL}/tasks/{path}", request, user_id)