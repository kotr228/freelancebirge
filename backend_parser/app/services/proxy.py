import httpx
import uuid
from fastapi import Request, Response, HTTPException
import logging

logger = logging.getLogger("parser_proxy")

async def base_proxy(target_url: str, request: Request, user_id: str = None):
    headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}
    
    request_id = request.headers.get("X-Request-ID")
    if not request_id:
        request_id = str(uuid.uuid4())
    
    headers["X-Request-ID"] = request_id

    if user_id:
        headers["X-User-ID"] = user_id

    # --- ЗМІНА ОСЬ ТУТ ---
    # Ми не читаємо і не передаємо тіло для GET та DELETE
    payload = None
    if request.method not in ["GET", "DELETE", "OPTIONS"]:
        payload = await request.body()
    # ---------------------

    timeout = httpx.Timeout(connect=5.0, read=15.0, write=5.0, pool=5.0)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            res = await client.request(
                method=request.method,
                url=target_url,
                content=payload,  # <--- Передаємо наш відфільтрований payload
                headers=headers,
                params=dict(request.query_params)
            )
            
            response_headers = dict(res.headers)
            response_headers["X-Request-ID"] = request_id
            
            return Response(content=res.content, status_code=res.status_code, headers=response_headers)
            
    except httpx.ConnectError:
        logger.error(f"[{request_id}] 🔥 Увага: Сервіс недоступний -> {target_url}")
        raise HTTPException(status_code=503, detail="Сервіс тимчасово недоступний.")
        
    except httpx.TimeoutException:
        logger.warning(f"[{request_id}] ⏳ Сервіс занадто довго відповідає -> {target_url}")
        raise HTTPException(status_code=504, detail="Перевищено час очікування від сервера.")
        
    except httpx.RequestError as e:
        logger.error(f"[{request_id}] ❌ Мережева помилка при запиті до {target_url}: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутрішня помилка шлюзу.")