"""Tests for InMemoryLoadRepository (Task A.3, requirement 11)."""

from datetime import datetime, timedelta, timezone

import pytest

from app.core.enums import CargoType, LoadStatus
from app.repositories.exceptions import NotFoundError
from app.repositories.models import GeoPoint

pytestmark = pytest.mark.asyncio


def _deadline():
    return datetime.now(timezone.utc) + timedelta(days=2)


async def test_create_and_get_by_id(load_repo):
    load = await load_repo.create(
        shipper_id="s-1",
        weight=500.0,
        cargo_type=CargoType.GENERAL,
        source=GeoPoint(lat=19.07, lng=72.87),
        destination=GeoPoint(lat=28.70, lng=77.10),
        deadline=_deadline(),
    )

    fetched = await load_repo.get_by_id(load.id)

    assert fetched is not None
    assert fetched.status == LoadStatus.POSTED
    assert fetched.shipper_id == "s-1"


async def test_get_by_id_returns_none_when_absent(load_repo):
    result = await load_repo.get_by_id("no-such-load")

    assert result is None


async def test_get_owner_id(load_repo):
    load = await load_repo.create(
        shipper_id="s-1", weight=100.0, cargo_type=CargoType.FRAGILE,
        source=GeoPoint(lat=0, lng=0), destination=GeoPoint(lat=1, lng=1),
        deadline=_deadline(),
    )

    owner_id = await load_repo.get_owner_id(load.id)

    assert owner_id == "s-1"


async def test_get_owner_id_raises_not_found(load_repo):
    with pytest.raises(NotFoundError):
        await load_repo.get_owner_id("no-such-load")


async def test_update_status(load_repo):
    load = await load_repo.create(
        shipper_id="s-1", weight=100.0, cargo_type=CargoType.HAZARDOUS,
        source=GeoPoint(lat=0, lng=0), destination=GeoPoint(lat=1, lng=1),
        deadline=_deadline(),
    )

    await load_repo.update_status(load.id, LoadStatus.ACCEPTED)

    fetched = await load_repo.get_by_id(load.id)
    assert fetched.status == LoadStatus.ACCEPTED


async def test_update_status_raises_not_found(load_repo):
    with pytest.raises(NotFoundError):
        await load_repo.update_status("no-such-load", LoadStatus.ACCEPTED)


async def test_list_open_only_returns_posted_loads(load_repo):
    open_load = await load_repo.create(
        shipper_id="s-1", weight=100.0, cargo_type=CargoType.GENERAL,
        source=GeoPoint(lat=0, lng=0), destination=GeoPoint(lat=1, lng=1),
        deadline=_deadline(),
    )
    accepted_load = await load_repo.create(
        shipper_id="s-1", weight=200.0, cargo_type=CargoType.GENERAL,
        source=GeoPoint(lat=0, lng=0), destination=GeoPoint(lat=1, lng=1),
        deadline=_deadline(),
    )
    await load_repo.update_status(accepted_load.id, LoadStatus.ACCEPTED)

    open_loads = await load_repo.list_open()

    open_ids = {l.id for l in open_loads}
    assert open_load.id in open_ids
    assert accepted_load.id not in open_ids
