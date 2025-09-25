# Running with Docker Compose

This project includes a minimal `docker-compose.yml` to run the Civitas backend together with a Postgres database for local development.

## Quick start

1. Copy the example env file:

   `cp .env.example .env`

2. Start services:

   `docker compose up --build`

This will build the app image and start:

- Postgres (on host port `5432`)
- FastAPI app (on host port `8000`)

## Notes

- The app uses environment variables `DB_HOST`, `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD`, `DB_NAME` to connect to Postgres. `.env.example` contains a matching configuration using `db` as the host (the compose service name).
- For a quick sqlite-only dev mode set `DEV_SQLITE=1` in `.env` and the app will use an in-memory sqlite DB instead.
- Postgres data is persisted in a named Docker volume `db_data`.
