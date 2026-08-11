FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip setuptools \
    && python -m pip install -r requirements.txt \
    && python -m pip install --upgrade "msgpack>=1.2.1" "setuptools>=78.1.1"

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY dashboard ./dashboard
COPY .env.example .

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]