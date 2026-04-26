# =============================================================================
# Development Dockerfile - Optimized for hot-reload and local editing
# =============================================================================
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# Install system dependencies (including git/curl for dev convenience)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies directly (no multi-stage for faster dev builds)
COPY src/requirements/ /app/src/requirements/
RUN pip install --no-cache-dir -r src/requirements/local.txt

# The code will be mounted as a volume in docker-compose.yml
# but we copy it here as a fallback
COPY . .

EXPOSE 8000

# Default command for development
CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]
