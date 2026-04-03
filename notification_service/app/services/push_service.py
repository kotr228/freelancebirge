async def send_push_task(push_token: str, title: str, body: str):
    if not push_token:
        return
    
    # Тут зазвичай логіка Firebase (FCM). Поки що робимо імітацію (Stub)
    # Коли буде готовий мобільний додаток, сюди вставимо реальний запит до FCM API
    print(f"📱 [PUSH SENT] Token: {push_token[:10]}... | {title}: {body}")