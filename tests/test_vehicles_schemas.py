from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.vehicles.schemas import GeoPoint, VehicleCreateRequest, VehicleType


def test_vehicle_create_requires_positive_capacity():
    with pytest.raises(ValidationError):
        VehicleCreateRequest(type=VehicleType.MINI_TRUCK, capacity_kg=0, capacity_volume=10)
    with pytest.raises(ValidationError):
        VehicleCreateRequest(type=VehicleType.MINI_TRUCK, capacity_kg=10, capacity_volume=-1)


def test_vehicle_create_route_pref_optional():
    req = VehicleCreateRequest(type=VehicleType.TRAILER, capacity_kg=5000, capacity_volume=20)
    assert req.route_pref is None


@pytest.mark.parametrize("lat,lng", [(91, 0), (-91, 0), (0, 181), (0, -181)])
def test_geopoint_rejects_out_of_range_coordinates(lat, lng):
    with pytest.raises(ValidationError):
        GeoPoint(lat=lat, lng=lng)


def test_geopoint_accepts_boundary_coordinates():
    GeoPoint(lat=90, lng=180)
    GeoPoint(lat=-90, lng=-180)
