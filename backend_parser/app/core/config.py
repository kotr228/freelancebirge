from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USER_SERVICE_URL: str = "http://user_service:8000"
    STORAGE_SERVICE_URL: str = "http://storage_service:8000"
    CHAT_SERVICE_URL: str = "http://chat_service:8000"
    TASK_SERVICE_URL: str = "http://task_manager_service:8000"
    NOTIFY_SERVICE_URL: str = "http://notification_service:8000"

    JWT_SECRET_KEY: str = "super_secret_birge_key_123" # В ідеалі це має братися з .env
    JWT_ALGORITHM: str = "HS256"

settings = Settings()