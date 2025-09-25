# Continuous Integration (GitLab)

This project includes a minimal GitLab CI pipeline (`.gitlab-ci.yml`) that is safe for beginners and useful for CI checks.

Jobs included:

- `lint` — runs `ruff check` against `src/`.
- `build` — builds a wheel using `python -m build` and uploads it as a short-lived artifact.
- `test:pytest` — runs `pytest` but is manual by default because tests may require Docker/Testcontainers.

How to run tests locally (recommended for noobs):

1. Create a virtual environment and install deps:

   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt

2. Run the tests:

   pytest -q

Enabling test job on GitLab:

- Provide a runner with Docker (or a shell runner where you installed Docker). The test suite uses testcontainers in places and may spin up a PostgreSQL container.
- In GitLab CI, go to the Pipeline page and run the `test:pytest` job manually (it's configured `when: manual`).

This keeps the pipeline from failing on shared runners without Docker while still allowing full test execution when you have a proper runner.
