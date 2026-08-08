from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.admin.schemas import AdminStatsOverviewResponse, RouteStat


def test_admin_stats_allows_all_zero_when_no_data_yet():
    resp = AdminStatsOverviewResponse(active=0, completed=0, delayed=0, revenue=0, top_routes=[])
    assert resp.top_routes == []


def test_admin_stats_rejects_negative_counts():
    with pytest.raises(ValidationError):
        AdminStatsOverviewResponse(active=-1, completed=0, delayed=0, revenue=0, top_routes=[])


def test_route_stat_rejects_negative_shipment_count():
    with pytest.raises(ValidationError):
        RouteStat(route="Mumbai -> Delhi", shipment_count=-5)
