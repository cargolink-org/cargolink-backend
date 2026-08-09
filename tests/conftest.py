"""
Shared pytest fixtures (Task A.1 pattern, reconstructed as a prerequisite
for A.3 — see note in app/core/enums.py).
"""

from __future__ import annotations

import pytest
from httpx import AsyncClient

from app.core import di
from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client


@pytest.fixture(autouse=True)
def _reset_di_registry():
    """
    Ensure every test starts with an empty DI registry, so tests that
    register repositories don't leak state into unrelated tests and tests
    that expect RepositoryNotRegisteredError don't accidentally see a
    previous test's registrations.
    """
    di.reset_registry()
    yield
    di.reset_registry()
