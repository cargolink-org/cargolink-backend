FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Production entrypoint mounts `socket_app`, NOT `app` — this is a
# specific, easy-to-get-wrong detail flagged repeatedly in the
# implementation guide (Cluster E.1 / I.2). Getting this wrong silently
# breaks only the Socket.io layer while REST endpoints keep working.
CMD ["gunicorn", "app.main:socket_app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
