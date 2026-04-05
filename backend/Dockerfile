FROM python:3.11-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Install dependencies via uv (uses uv.lock for reproducible installs)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy source and install the project package
COPY src/ ./src/
RUN uv sync --frozen --no-dev

ENV PYTHONPATH=/app/src
ENV PATH="/app/.venv/bin:$PATH"

# Expose FastAPI default port
EXPOSE 8000

# Run custom entrypoint that prepares the DB then execs uvicorn
CMD ["python", "-m", "backend.entrypoint"]
