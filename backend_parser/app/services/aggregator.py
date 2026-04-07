import httpx
from ..core.config import settings

class DataAggregator:
    @staticmethod
    async def get_full_task_details(task_id: str):
        async with httpx.AsyncClient() as client:
            # 1. Отримуємо саму задачу
            task_res = await client.get(f"{settings.TASK_SERVICE_URL}/tasks/{task_id}")
            if task_res.status_code != 200:
                return None
            task_data = task_res.json()

            # 2. Паралельно беремо дані замовника та його аватар
            employer_id = task_data["employer_id"]
            user_res = await client.get(f"{settings.USER_SERVICE_URL}/users/{employer_id}")
            storage_res = await client.get(f"{settings.STORAGE_SERVICE_URL}/files/avatar/{employer_id}")

            # Збираємо все в один об'єкт
            task_data["employer_name"] = user_res.json().get("username", "Unknown") if user_res.status_code == 200 else "Unknown"
            task_data["employer_avatar"] = storage_res.json().get("url") if storage_res.status_code == 200 else None
            
            return task_data

aggregator = DataAggregator()