"""Tests for InMemoryLocationPingRepository (Task A.3, requirement 11)."""

from datetime import datetime, timedelta, timezone

import pytest

pytestmark = pytest.mark.asyncio


def _ts(offset_minutes=0):
    return datetime.now(timezone.utc) + timedelta(minutes=offset_minutes)


async def test_get_latest_returns_none_when_no_pings(location_ping_repo):
    result = await location_ping_repo.get_latest("vehicle-1")

    assert result is None


async def test_create_and_get_latest(location_ping_repo):
    await location_ping_repo.create("vehicle-1", lat=19.0, lng=72.0, ts=_ts(0))
    latest_ts = _ts(5)
    await location_ping_repo.create("vehicle-1", lat=19.1, lng=72.1, ts=latest_ts)

    latest = await location_ping_repo.get_latest("vehicle-1")

    assert latest.ts == latest_ts
    assert latest.lat == 19.1


async def test_list_for_vehicle_returns_all_when_no_bounds(location_ping_repo):
    await location_ping_repo.create("vehicle-1", lat=19.0, lng=72.0, ts=_ts(0))
    await location_ping_repo.create("vehicle-1", lat=19.1, lng=72.1, ts=_ts(5))

    pings = await location_ping_repo.list_for_vehicle("vehicle-1")

    assert len(pings) == 2


async def test_list_for_vehicle_filters_by_from_and_to(location_ping_repo):
    await location_ping_repo.create("vehicle-1", lat=19.0, lng=72.0, ts=_ts(0))
    middle_ts = _ts(5)
    await location_ping_repo.create("vehicle-1", lat=19.1, lng=72.1, ts=middle_ts)
    await location_ping_repo.create("vehicle-1", lat=19.2, lng=72.2, ts=_ts(10))

    pings = await location_ping_repo.list_for_vehicle(
        "vehicle-1", from_ts=_ts(2), to_ts=_ts(7)
    )

    assert len(pings) == 1
    assert pings[0].ts == middle_ts


async def test_list_for_vehicle_empty_for_unknown_vehicle(location_ping_repo):
    pings = await location_ping_repo.list_for_vehicle("no-such-vehicle")

    assert pings == []
