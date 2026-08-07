"""
Smoke test for Task A.1.

Proves the ASGI app boots and serves traffic with ZERO live database,
OSRM, SMS/email provider, or S3 configuration -- the explicit Sprint 1
acceptance criteria -- and that Swagger UI (/docs) is reachable.
"""
import httpx
import pytest

from app.main import app, socket_app


@pytest.mark.asyncio
async def test_health_endpoint_reports_ok_and_mock_mode() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    # Default local/test config runs against mocks -- this is the whole point.
    assert body["mock_repo"] is True


@pytest.mark.asyncio
async def test_docs_swagger_ui_reachable() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/docs")

    assert response.status_code == 200
    assert "swagger" in response.text.lower()


@pytest.mark.asyncio
async def test_openapi_schema_is_generated() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/openapi.json")

    assert response.status_code == 200
    schema = response.json()
    assert schema["info"]["title"] == "CargoLink Backend"


@pytest.mark.asyncio
async def test_unhandled_exception_returns_standard_error_shape_without_traceback() -> None:
    @app.get("/__test_boom")
    async def boom():
        raise ValueError("intentional test failure — should never reach the client")

    transport = httpx.ASGITransport(app=app, raise_app_exceptions=False)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/__test_boom")

    assert response.status_code == 500
    body = response.json()
    assert body == {
        "error": {
            "code": "internal_server_error",
            "message": "An unexpected error occurred. Please try again later.",
        }
    }
    # No raw exception detail should leak into the response body.
    assert "ValueError" not in response.text
    assert "intentional test failure" not in response.text


def test_socket_app_is_the_correct_deployed_entrypoint() -> None:
    """
    Cluster E and Task I.2 both flag this exact footgun: `socket_app`, not
    `app`, must be the ASGI entrypoint. This guards the wiring so a future
    refactor can't silently regress it.
    """
    import socketio

    assert isinstance(socket_app, socketio.ASGIApp)
    assert socket_app.other_asgi_app is app
