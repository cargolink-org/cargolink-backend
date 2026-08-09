"""Tests for InMemoryLoadMatchRepository (Task A.3, requirement 11).

LoadMatchRepository is one of the four ConflictError-raising repositories
(requirement 5): create() raises ConflictError if the vehicle already has
an active (PROPOSED/ACCEPTED) match for a *different* load — the "match
no longer available" race.
"""

import pytest

from app.core.enums import LoadMatchStatus
from app.repositories.exceptions import ConflictError, NotFoundError

pytestmark = pytest.mark.asyncio


async def test_create_and_get_by_load_and_vehicle(load_match_repo):
    match = await load_match_repo.create(
        load_id="load-1", vehicle_id="vehicle-1", status=LoadMatchStatus.PROPOSED, match_score=0.9
    )

    fetched = await load_match_repo.get_by_load_and_vehicle("load-1", "vehicle-1")

    assert fetched is not None
    assert fetched.id == match.id


async def test_get_by_load_and_vehicle_returns_none_when_absent(load_match_repo):
    result = await load_match_repo.get_by_load_and_vehicle("load-1", "vehicle-1")

    assert result is None


async def test_create_conflict_when_vehicle_already_active_on_different_load(load_match_repo):
    await load_match_repo.create(
        load_id="load-1", vehicle_id="vehicle-1", status=LoadMatchStatus.PROPOSED, match_score=0.9
    )

    with pytest.raises(ConflictError):
        await load_match_repo.create(
            load_id="load-2", vehicle_id="vehicle-1", status=LoadMatchStatus.PROPOSED, match_score=0.8
        )


async def test_create_allows_same_vehicle_multiple_proposals_on_same_load(load_match_repo):
    # Not a conflict: same (load_id, vehicle_id) pair re-proposed (e.g. a
    # re-run of the matching engine) is not the cross-load race this rule
    # guards against.
    await load_match_repo.create(
        load_id="load-1", vehicle_id="vehicle-1", status=LoadMatchStatus.PROPOSED, match_score=0.9
    )
    second = await load_match_repo.create(
        load_id="load-1", vehicle_id="vehicle-1", status=LoadMatchStatus.PROPOSED, match_score=0.95
    )

    assert second.load_id == "load-1"


async def test_create_allows_new_match_after_prior_one_rejected(load_match_repo):
    first = await load_match_repo.create(
        load_id="load-1", vehicle_id="vehicle-1", status=LoadMatchStatus.PROPOSED, match_score=0.9
    )
    await load_match_repo.update_status(first.id, LoadMatchStatus.REJECTED)

    # Vehicle is free again since its only match is now REJECTED (inactive).
    second = await load_match_repo.create(
        load_id="load-2", vehicle_id="vehicle-1", status=LoadMatchStatus.PROPOSED, match_score=0.7
    )

    assert second.load_id == "load-2"


async def test_update_status(load_match_repo):
    match = await load_match_repo.create(
        load_id="load-1", vehicle_id="vehicle-1", status=LoadMatchStatus.PROPOSED, match_score=0.9
    )

    await load_match_repo.update_status(match.id, LoadMatchStatus.ACCEPTED)

    fetched = await load_match_repo.get_by_load_and_vehicle("load-1", "vehicle-1")
    assert fetched.status == LoadMatchStatus.ACCEPTED


async def test_update_status_raises_not_found(load_match_repo):
    with pytest.raises(NotFoundError):
        await load_match_repo.update_status("no-such-match", LoadMatchStatus.ACCEPTED)


async def test_list_by_load(load_match_repo):
    await load_match_repo.create(
        load_id="load-1", vehicle_id="vehicle-1", status=LoadMatchStatus.PROPOSED, match_score=0.9
    )
    await load_match_repo.create(
        load_id="load-1", vehicle_id="vehicle-2", status=LoadMatchStatus.PROPOSED, match_score=0.5
    )
    await load_match_repo.create(
        load_id="load-2", vehicle_id="vehicle-3", status=LoadMatchStatus.PROPOSED, match_score=0.5
    )

    matches = await load_match_repo.list_by_load("load-1")

    assert len(matches) == 2
    assert {m.vehicle_id for m in matches} == {"vehicle-1", "vehicle-2"}
