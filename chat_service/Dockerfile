FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Оновлюємо pip до останньої версії всередині контейнера
RUN pip install --upgrade pip

COPY requirements.txt .
# Додаємо тайм-аут, щоб pip не здавався занадто швидко
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]