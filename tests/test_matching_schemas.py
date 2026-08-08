from __future__ import annotations

from uuid import uuid4

from app.matching.schemas import LoadMatchesResponse, MatchCandidate


def test_load_matches_response_allows_empty_list():
    resp = LoadMatchesResponse(matches=[])
    assert resp.matches == []


def test_match_candidate_round_trip():
    candidate = MatchCandidate(vehicle_id=uuid4(), distance_km=12.5, capacity_fit=True, eta=900, score=0.87)
    assert candidate.distance_km == 12.5
    assert candidate.capacity_fit is True
