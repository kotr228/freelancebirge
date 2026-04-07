import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .config import settings

# Вказуємо FastAPI, що ми використовуємо Bearer токени
security = HTTPBearer()

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> str:
    """
    Перевіряє токен. Якщо все ок — повертає user_id (з поля 'sub').
    Якщо ні — викидає 401 помилку.
    """
    token = credentials.credentials
    try:
        # Розшифровуємо токен
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub") # "sub" (subject) зазвичай зберігає ID юзера
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return user_id
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")