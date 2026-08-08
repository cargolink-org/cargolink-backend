from __future__ import annotations

from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.ratings.schemas import RatingCreateRequest


def test_rating_comment_is_optional():
    req = RatingCreateRequest(load_id=uuid4(), ratee_id=uuid4(), score=5)
    assert req.comment is None


@pytest.mark.parametrize("score", [0, 6, -1])
def test_rating_score_must_be_within_one_to_five(score):
    with pytest.raises(ValidationError):
        RatingCreateRequest(load_id=uuid4(), ratee_id=uuid4(), score=score)


@pytest.mark.parametrize("score", [1, 3, 5])
def test_rating_score_boundary_values_are_valid(score):
    req = RatingCreateRequest(load_id=uuid4(), ratee_id=uuid4(), score=score)
    assert req.score == score
