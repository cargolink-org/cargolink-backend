"""Tests for InMemoryRatingRepository (Task A.3, requirement 11).

RatingRepository is one of the four ConflictError-raising repositories
(requirement 5): create() raises ConflictError on a duplicate
(load_id, rater_id, ratee_id) triple.
"""

import pytest

from app.repositories.exceptions import ConflictError

pytestmark = pytest.mark.asyncio


async def test_create_and_list_for_ratee(rating_repo):
    rating = await rating_repo.create(
        load_id="load-1", rater_id="shipper-1", ratee_id="transporter-1", score=5, comment="Great!"
    )

    ratings = await rating_repo.list_for_ratee("transporter-1")

    assert ratings == [rating]


async def test_exists_false_before_creation(rating_repo):
    exists = await rating_repo.exists("load-1", "shipper-1", "transporter-1")

    assert exists is False


async def test_exists_true_after_creation(rating_repo):
    await rating_repo.create(
        load_id="load-1", rater_id="shipper-1", ratee_id="transporter-1", score=5, comment=None
    )

    exists = await rating_repo.exists("load-1", "shipper-1", "transporter-1")

    assert exists is True


async def test_create_raises_conflict_on_duplicate_triple(rating_repo):
    await rating_repo.create(
        load_id="load-1", rater_id="shipper-1", ratee_id="transporter-1", score=5, comment=None
    )

    with pytest.raises(ConflictError):
        await rating_repo.create(
            load_id="load-1", rater_id="shipper-1", ratee_id="transporter-1", score=1, comment="Changed my mind"
        )


async def test_create_allows_reverse_rating_same_load(rating_repo):
    # The transporter rating the shipper is a DIFFERENT triple (rater and
    # ratee swapped) — both parties rate each other post-trip.
    await rating_repo.create(
        load_id="load-1", rater_id="shipper-1", ratee_id="transporter-1", score=5, comment=None
    )
    reverse = await rating_repo.create(
        load_id="load-1", rater_id="transporter-1", ratee_id="shipper-1", score=4, comment=None
    )

    assert reverse.rater_id == "transporter-1"


async def test_list_for_ratee_only_returns_matching_ratee(rating_repo):
    await rating_repo.create(
        load_id="load-1", rater_id="shipper-1", ratee_id="transporter-1", score=5, comment=None
    )
    await rating_repo.create(
        load_id="load-2", rater_id="shipper-2", ratee_id="transporter-2", score=3, comment=None
    )

    ratings = await rating_repo.list_for_ratee("transporter-1")

    assert len(ratings) == 1
    assert ratings[0].ratee_id == "transporter-1"
