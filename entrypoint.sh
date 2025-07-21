#!/bin/bash

python3 -m alembic upgrade head
exec uvicorn src.main:app --host 0.0.0.0 --port 8000