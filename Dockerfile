# =============================================================================
# STAGE 1: Dependency builder
# =============================================================================
FROM python:3.12-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvbin/uv
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/uvbin:$PATH"

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev && \
    uv add gunicorn

# =============================================================================
# STAGE 2: Non-root runtime
# =============================================================================
FROM python:3.12-slim-bookworm AS runner

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    DJANGO_ENV=prod \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN groupadd -g 1000 django && \
    useradd -u 1000 -g django -m -s /bin/bash django && \
    apt-get update && apt-get install -y --no-install-recommends libpq5 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder --chown=django:django /app/.venv /app/.venv
COPY --chown=django:django src ./src

USER django

EXPOSE 8080

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-8080} --workers 4 --chdir src config.wsgi:application"]
