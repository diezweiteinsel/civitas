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

Navigate to the root folder of the project and create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
# navigate to backend
cd backend  # On Windows use `venv\Scripts\activate`
pip install -r requirements-linux.txt # or requirements.txt
```

Next, install the package of the application:

```bash
pip install -e .
```

This will install the package in "editable" mode, meaning that changes to the source code will be reflected without needing to reinstall the package.

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