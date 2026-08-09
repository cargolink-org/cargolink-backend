"""Tests for InMemoryContainerRepository (Task A.3, requirement 11)."""

import pytest

pytestmark = pytest.mark.asyncio


async def test_get_by_load_returns_none_for_road_only_load(container_repo):
    # F.3 edge case: must not raise for a load with no container data.
    result = await container_repo.get_by_load("load-1")

    assert result is None


async def test_upsert_and_get_by_load(container_repo):
    container = await container_repo.upsert(
        load_id="load-1",
        container_no="MSCU1234567",
        vessel_or_flight="MV Example",
        port_of_loading="INNSA",
        port_of_discharge="USLAX",
    )

    fetched = await container_repo.get_by_load("load-1")

    assert fetched == container


async def test_upsert_updates_existing_record(container_repo):
    await container_repo.upsert(
        load_id="load-1", container_no="MSCU1234567", vessel_or_flight="MV Example",
        port_of_loading="INNSA", port_of_discharge="USLAX",
    )

    updated = await container_repo.upsert(
        load_id="load-1", container_no="MSCU7654321", vessel_or_flight="MV Other",
        port_of_loading="INNSA", port_of_discharge="USLAX",
    )

    fetched = await container_repo.get_by_load("load-1")
    assert fetched.container_no == "MSCU7654321"
    assert fetched == updated
