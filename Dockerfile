FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python3 -m alembic upgrade head; uvicorn src.main:app --host 0.0.0.0 --port 8000