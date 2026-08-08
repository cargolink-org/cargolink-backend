from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.loads.schemas import CargoType, LoadCreateRequest
from app.vehicles.schemas import GeoPoint


def _valid_kwargs(**overrides):
    kwargs = dict(
        weight=1000,
        cargo_type=CargoType.GENERAL,
        source=GeoPoint(lat=19.076, lng=72.8777),
        destination=GeoPoint(lat=28.7041, lng=77.1025),
        deadline=datetime.now(timezone.utc),
    )
    kwargs.update(overrides)
    return kwargs


def test_load_create_accepts_all_cargo_types():
    for cargo_type in CargoType:
        LoadCreateRequest(**_valid_kwargs(cargo_type=cargo_type))


def test_load_create_rejects_unknown_cargo_type():
    with pytest.raises(ValidationError):
        LoadCreateRequest(**_valid_kwargs(cargo_type="explosive"))


def test_load_create_requires_positive_weight():
    with pytest.raises(ValidationError):
        LoadCreateRequest(**_valid_kwargs(weight=0))


def test_load_create_requires_deadline():
    kwargs = _valid_kwargs()
    del kwargs["deadline"]
    with pytest.raises(ValidationError):
        LoadCreateRequest(**kwargs)
