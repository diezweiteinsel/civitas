# Continuous Integration (GitHub Actions)

This project uses GitHub Actions. The workflow files live in `.github/workflows/`.

## Workflows

| File | Trigger | Purpose |
|---|---|---|
| `ci.yml` | every push / PR | lint, pytest, Jest, sanity Docker builds |
| `deploy.yml` | CI passes on `main`, or manual | SSH deploy to VM |
| `reset-deployment.yml` | manual (`workflow_dispatch`) | `docker compose down -v` + restart on VM |

## Running tests locally

1. Install deps (including dev group):

   ```
   uv sync
   ```
   (run from `backend/`)

2. Run the tests:

   ```
   uv run pytest -q
   ```

   The backend test suite requires a running PostgreSQL instance. The easiest way is:

   ```
   docker compose up db -d
   DATABASE_URL=postgresql://civitas_user:securepassword@localhost:5432/civitas_db uv run pytest -q
   ```

## Required GitHub Secrets

Set these in **Settings → Secrets and variables → Actions** (repository or environment `production`):

| Secret | Description |
|---|---|
| `SSH_PRIVATE_KEY` | OpenSSH private key for the deploy VM (no passphrase) |
| `SSH_PORT` | SSH port on the VM |
| `SSH_USER` | SSH username on the VM |
| `SSH_SERVER_IP` | IP address of the VM |
| `VM_DEPLOY_PATH` | Absolute path on the VM where the app is deployed |
| `POSTGRES_DB` | Production database name |
| `POSTGRES_USER` | Production database user |
| `POSTGRES_PASSWORD` | Production database password |
| `SECRET_KEY` | JWT secret key |
| `ALGORITHM` | JWT algorithm (e.g. `HS256`) |
| `ALLOWED_ORIGINS` | CORS allowed origins for the backend |

This keeps the pipeline from failing on shared runners without Docker while still allowing full test execution when you have a proper runner.
