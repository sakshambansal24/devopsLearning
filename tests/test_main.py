import pytest
import httpx

from app.main import create_app


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.mark.anyio
async def test_health() -> None:
    app = create_app("sqlite+pysqlite:///:memory:")

    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_create_and_list_users() -> None:
    app = create_app("sqlite+pysqlite:///:memory:")

    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            create_response = await client.post(
                "/users",
                json={"name": "Saksham", "email": "saksham@example.com"},
            )
            list_response = await client.get("/users")

    assert create_response.status_code == 201
    assert create_response.json()["name"] == "Saksham"
    assert create_response.json()["email"] == "saksham@example.com"

    assert list_response.status_code == 200
    assert len(list_response.json()) == 1
    assert list_response.json()[0]["email"] == "saksham@example.com"


@pytest.mark.anyio
async def test_duplicate_email_returns_conflict() -> None:
    app = create_app("sqlite+pysqlite:///:memory:")

    async with app.router.lifespan_context(app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            first_response = await client.post(
                "/users",
                json={"name": "One", "email": "same@example.com"},
            )
            duplicate_response = await client.post(
                "/users",
                json={"name": "Two", "email": "same@example.com"},
            )

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 409
