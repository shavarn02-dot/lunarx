FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=0

WORKDIR /app

# System dependencies for OpenCV & git for LightGlue
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Layer 1: Cached dependencies (only rebuilds if requirements.txt changes)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Layer 2: Application source code (rebuilds in seconds when code changes)
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.api_server:app --host 0.0.0.0 --port ${PORT:-8000}"]
