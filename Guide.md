# How to start the application

## Pre-requisites

- Python 3.11 or higher
- Docker installed (with Docker Compose)
- Git installed


### Cloning the Repository

Clone the full repository:
https://cau-git.rz.uni-kiel.de/ifi-ag-se/softwareprojekt/lms8_eg_017/civitas

```bash
git clone https://cau-git.rz.uni-kiel.de/ifi-ag-se/softwareprojekt/lms8_eg_017/civitas.git
```

### Setting up the Environment

You need to create an `.env` file in the root directory of the project. You can copy these contents into the `.env` file:

```bash
# .env file
DB_HOST=db
DB_PORT=5432
DB_NAME=civitas_db
DB_USERNAME=civitas_user
DB_PASSWORD=securepassword
SECRET_KEY=bazooks-itsa-jetlag-season-guys
ALGORITHM=HS256
DEV_SQLITE=0
SKIP_CREATE_ALL=0
ECHO_SQL=1
PYTHONPATH=/app
```

### Setting up the Python Environment

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. Install it once:

```bash
# macOS / Linux
curl -Ls https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then install all dependencies (including dev tools) from the lockfile:

```bash
cd backend
uv sync
```

This creates a `.venv` and installs everything. Changes to the source code are reflected immediately — no reinstall needed.

### Running the Application

```bash
docker compose up -d --build
```

`localhost` - Frontend
`localhost:8000/api/v1` - Backend API, Swagger UI at `localhost:8000/api/v1/docs`


### What you will find on our playground 🏕️🗽

- You can register a new user with email & password
- You can login with that user and receive a JWT token
- You can checkout our current UI

- You can, optionally, use our demo user:
- username: `demo`
- password: `demo`

#### Inside the API documentation (Swagger UI)

All the endpoints are already documented, but almost none of them work. You can do this tho:

- Create a new user via `POST /users/` (register)
- Login via `POST /auth/` (login) to receive a token
- Get all users via `GET /users/`