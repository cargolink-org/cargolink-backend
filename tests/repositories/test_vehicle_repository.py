"""Tests for InMemoryVehicleRepository (Task A.3, requirement 11).

VehicleRepository operations raise NotFoundError for an unknown
vehicle_id (requirement 5) — covered for update_location and
is_available below.
"""

from datetime import datetime, timezone

import pytest

from app.core.enums import VehicleType
from app.repositories.exceptions import NotFoundError
from app.repositories.models import GeoPoint

pytestmark = pytest.mark.asyncio


async def test_create_and_get_by_id(vehicle_repo):
    vehicle = await vehicle_repo.create(
        transporter_id="t-1",
        type=VehicleType.MINI_TRUCK,
        capacity_kg=1000.0,
        capacity_volume=None,
        route_pref=None,
    )

    fetched = await vehicle_repo.get_by_id(vehicle.id)

    assert fetched is not None
    assert fetched.transporter_id == "t-1"
    assert fetched.capacity_kg == 1000.0


async def test_get_by_id_returns_none_when_absent(vehicle_repo):
    result = await vehicle_repo.get_by_id("no-such-vehicle")

    assert result is None


async def test_list_by_transporter(vehicle_repo):
    v1 = await vehicle_repo.create(
        transporter_id="t-1", type=VehicleType.TRAILER, capacity_kg=5000.0,
        capacity_volume=None, route_pref=None,
    )
    await vehicle_repo.create(
        transporter_id="t-2", type=VehicleType.TRAILER, capacity_kg=5000.0,
        capacity_volume=None, route_pref=None,
    )

    vehicles = await vehicle_repo.list_by_transporter("t-1")

    assert [v.id for v in vehicles] == [v1.id]


async def test_update_location_raises_not_found(vehicle_repo):
    with pytest.raises(NotFoundError):
        await vehicle_repo.update_location(
            "no-such-vehicle", lat=19.07, lng=72.87, ts=datetime.now(timezone.utc)
        )


async def test_update_location_sets_current_location(vehicle_repo):
    vehicle = await vehicle_repo.create(
        transporter_id="t-1", type=VehicleType.CONTAINER_TRUCK, capacity_kg=8000.0,
        capacity_volume=None, route_pref=None,
    )
    ts = datetime.now(timezone.utc)

    await vehicle_repo.update_location(vehicle.id, lat=19.07, lng=72.87, ts=ts)

    fetched = await vehicle_repo.get_by_id(vehicle.id)
    assert fetched.current_location == GeoPoint(lat=19.07, lng=72.87)
    assert fetched.last_ping_at == ts


async def test_is_available_raises_not_found(vehicle_repo):
    with pytest.raises(NotFoundError):
        await vehicle_repo.is_available("no-such-vehicle")


async def test_is_available_defaults_true(vehicle_repo):
    vehicle = await vehicle_repo.create(
        transporter_id="t-1", type=VehicleType.OTHER, capacity_kg=100.0,
        capacity_volume=None, route_pref=None,
    )

    assert await vehicle_repo.is_available(vehicle.id) is True


async def test_find_within_radius_filters_by_capacity_and_distance(vehicle_repo):
    near_enough = await vehicle_repo.create(
        transporter_id="t-1", type=VehicleType.MINI_TRUCK, capacity_kg=2000.0,
        capacity_volume=None, route_pref=None,
    )
    await vehicle_repo.update_location(near_enough.id, lat=19.076, lng=72.8777, ts=datetime.now(timezone.utc))

    too_small = await vehicle_repo.create(
        transporter_id="t-2", type=VehicleType.MINI_TRUCK, capacity_kg=100.0,
        capacity_volume=None, route_pref=None,
    )
    await vehicle_repo.update_location(too_small.id, lat=19.076, lng=72.8777, ts=datetime.now(timezone.utc))

    too_far = await vehicle_repo.create(
        transporter_id="t-3", type=VehicleType.MINI_TRUCK, capacity_kg=2000.0,
        capacity_volume=None, route_pref=None,
    )
    # Delhi — hundreds of km from the Mumbai pickup point below.
    await vehicle_repo.update_location(too_far.id, lat=28.7041, lng=77.1025, ts=datetime.now(timezone.utc))

    no_location = await vehicle_repo.create(
        transporter_id="t-4", type=VehicleType.MINI_TRUCK, capacity_kg=2000.0,
        capacity_volume=None, route_pref=None,
    )

    pickup_point = GeoPoint(lat=19.0760, lng=72.8777)  # Mumbai
    results = await vehicle_repo.find_within_radius(pickup_point, radius_km=50, min_capacity_kg=1000)

    result_ids = {v.id for v in results}
    assert near_enough.id in result_ids
    assert too_small.id not in result_ids
    assert too_far.id not in result_ids
    assert no_location.id not in result_ids


async def test_find_within_radius_empty_when_no_match(vehicle_repo):
    pickup_point = GeoPoint(lat=19.0760, lng=72.8777)

    results = await vehicle_repo.find_within_radius(pickup_point, radius_km=10, min_capacity_kg=1000)

    assert results == []
