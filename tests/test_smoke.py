"""Smoke tests — app boots and Swagger UI is reachable.

Treated as pre-existing per A.1, recreated here since it was not found in
this sandbox. Proves the "zero live database, zero live OSRM, zero live
SMS/email provider" boot requirement from A.1's acceptance criteria, and
gives A.2 a template for how this project's tests call the app.
"""
from __future__ import annotations

import pytest


@pytest.mark.asyncio
async def test_app_boots_and_docs_reachable(client):
    response = await client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_openapi_json_is_served(client):
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    body = response.json()
    assert body["info"]["title"] == "CargoLink Backend"
