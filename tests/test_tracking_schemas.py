from __future__ import annotations

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.tracking.schemas import LocationPoint, TrackingHistoryResponse


def test_location_point_rejects_out_of_range_lat():
    with pytest.raises(ValidationError):
        LocationPoint(lat=91, lng=0, timestamp=datetime.now(timezone.utc))


def test_tracking_history_response_allows_empty_points():
    resp = TrackingHistoryResponse(points=[])
    assert resp.points == []
