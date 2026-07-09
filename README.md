# FastAPI DevOps Demo

A small FastAPI project backed by Postgres. It is intentionally simple so you can use it to learn CI/CD.

## Endpoints

- `GET /health` - service health check
- `POST /users` - create a user
- `GET /users` - list users

Example user payload:

```json
{
  "name": "Saksham",
  "email": "saksham@example.com"
}
```

## Run Locally With Docker

```bash
docker compose up --build
```

Then open:

- API: `http://localhost:8001`
- Docs: `http://localhost:8001/docs`
- Health: `http://localhost:8001/health`

## Run Tests

```bash
pip install -r requirements-dev.txt
pytest
```

Tests use SQLite in memory so they do not require Postgres.

## Useful Commands

```bash
make install
make test
make lint
make compose-up
make compose-down
```

## Environment

For local non-Docker runs, set:

```bash
DATABASE_URL=postgresql+psycopg2://app_user:app_password@localhost:5432/app_db
```

The Docker Compose setup already provides this value inside the API container.
