# CargoLink backend — production image
# Deploys `app.main:socket_app` (FastAPI + python-socketio combined ASGI app),
# NOT `app.main:app` alone — see app/main.py's module docstring for why
# that distinction matters (it silently breaks only the real-time layer).

FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# build-essential: needed for source builds of some deps (e.g. asyncpg on
# less common platforms); curl: used by the HEALTHCHECK below.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Sane production defaults. Real secrets (DATABASE_URL, JWT_SECRET_KEY,
# S3/MSG91/SendGrid credentials, SENTRY_DSN) must be injected by the
# hosting platform's environment configuration — never baked into the
# image. MOCK_REPO=false is a hard requirement here; app/core/config.py
# will refuse to start in ENVIRONMENT=production with mocks enabled.
ENV ENVIRONMENT=production \
    MOCK_REPO=false \
    DEBUG=false

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["gunicorn", "app.main:socket_app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
