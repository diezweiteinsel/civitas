FROM python:3.11-slim

WORKDIR /app

# Install build deps and runtime deps
COPY pyproject.toml .
COPY requirements-linux.txt .
RUN pip install --no-cache-dir -r requirements-linux.txt

# Copy source
COPY src/ ./src/

# Install the project package so `backend` is importable inside the image
# The project's pyproject.toml is at the repository root and declares packages in `src`.
RUN pip install --no-cache-dir .

ENV PYTHONPATH=/app/src

# Expose FastAPI default port
EXPOSE 8000

# Run custom entrypoint that prepares the DB then execs uvicorn
CMD ["python", "-m", "backend.entrypoint"]
