FROM python:3.13-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

COPY --chmod=755 --chown=appuser:appuser scripts/ ./scripts/
COPY . .

RUN chmod +x scripts/*.sh

RUN useradd -m appuser \
    && chown -R appuser:appuser /app

ENV PYTHONPATH=/app/src \
    PATH="/app/.venv/bin:$PATH"

USER appuser