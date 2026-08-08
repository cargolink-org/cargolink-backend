"""Shared pytest fixtures.

Treated as pre-existing per A.1 ("tests/test_smoke.py for the pattern"),
recreated here since it was not found in this sandbox. Provides an `app`
fixture (fresh FastAPI instance per test, built via create_app()) and a
`client` fixture (httpx.AsyncClient over ASGITransport, no real network/
server process needed).
"""
from __future__ import annotations

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import create_app


@pytest.fixture
def app():
    return create_app()


@pytest_asyncio.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
