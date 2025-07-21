FROM python:3.12.6-slim-bullseye AS builder

WORKDIR /app

RUN apt update -y && \
    apt install -y --no-install-recommends python3-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT="/usr/local/"

RUN pip install uv==0.7.6

COPY ./pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

FROM python:3.12.6-slim-bullseye AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT="/usr/local/"

COPY --from=builder /usr/local /usr/local

COPY . .

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]