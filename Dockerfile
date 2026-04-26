# =============================================================================
# STAGE 1: Builder
# =============================================================================
FROM python:3.12-slim-bookworm AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvbin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/uvbin:$PATH"

WORKDIR /app

# Install dependencies first (caching layer)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy the rest of the project
COPY . .

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# =============================================================================
# STAGE 2: Runner
# =============================================================================
FROM python:3.12-slim-bookworm AS runner

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# Create non-root user
RUN groupadd -g 1000 django && \
    useradd -u 1000 -g django -m -s /bin/bash django

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder --chown=django:django /app/.venv /app/.venv
# Copy source code
COPY --chown=django:django . .

# Path to uv-installed binaries
ENV PATH="/app/.venv/bin:$PATH"

USER django

EXPOSE 8080

# Use Gunicorn as process manager
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 4 --chdir src config.wsgi:application"]
