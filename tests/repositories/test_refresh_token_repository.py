"""Tests for InMemoryRefreshTokenRepository (Task A.3, requirement 11).

RefreshTokenRepository is one of the four ConflictError-raising
repositories (requirement 5): mark_rotated() raises ConflictError when a
token is reused after rotation — this is the theft-detection signal.
"""

from datetime import datetime, timedelta, timezone

import pytest

from app.repositories.exceptions import ConflictError, NotFoundError

pytestmark = pytest.mark.asyncio


def _future(minutes=30):
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)


async def test_create_and_get(refresh_token_repo):
    expires_at = _future()
    await refresh_token_repo.create(
        user_id="user-1", token="tok-a", family_id="fam-1", expires_at=expires_at
    )

    record = await refresh_token_repo.get("tok-a")

    assert record is not None
    assert record.user_id == "user-1"
    assert record.family_id == "fam-1"
    assert record.rotated is False
    assert record.invalidated is False


async def test_get_returns_none_when_absent(refresh_token_repo):
    result = await refresh_token_repo.get("does-not-exist")

    assert result is None


async def test_is_valid_true_for_fresh_token(refresh_token_repo):
    await refresh_token_repo.create(
        user_id="user-1", token="tok-a", family_id="fam-1", expires_at=_future()
    )

    assert await refresh_token_repo.is_valid("tok-a") is True


async def test_is_valid_false_for_unknown_token(refresh_token_repo):
    assert await refresh_token_repo.is_valid("never-issued") is False


async def test_is_valid_false_for_expired_token(refresh_token_repo):
    expired = datetime.now(timezone.utc) - timedelta(minutes=1)
    await refresh_token_repo.create(
        user_id="user-1", token="tok-a", family_id="fam-1", expires_at=expired
    )

    assert await refresh_token_repo.is_valid("tok-a") is False


async def test_mark_rotated_creates_new_token_in_same_family(refresh_token_repo):
    await refresh_token_repo.create(
        user_id="user-1", token="tok-a", family_id="fam-1", expires_at=_future()
    )

    await refresh_token_repo.mark_rotated("tok-a", "tok-b")

    old = await refresh_token_repo.get("tok-a")
    new = await refresh_token_repo.get("tok-b")
    assert old.rotated is True
    assert new is not None
    assert new.family_id == "fam-1"
    assert await refresh_token_repo.is_valid("tok-a") is False
    assert await refresh_token_repo.is_valid("tok-b") is True


async def test_mark_rotated_raises_not_found_for_unknown_token(refresh_token_repo):
    with pytest.raises(NotFoundError):
        await refresh_token_repo.mark_rotated("never-issued", "tok-b")


async def test_mark_rotated_twice_raises_conflict_reuse_detection(refresh_token_repo):
    await refresh_token_repo.create(
        user_id="user-1", token="tok-a", family_id="fam-1", expires_at=_future()
    )
    await refresh_token_repo.mark_rotated("tok-a", "tok-b")

    # Presenting the already-rotated tok-a again is the reuse/theft signal.
    with pytest.raises(ConflictError):
        await refresh_token_repo.mark_rotated("tok-a", "tok-c")


async def test_invalidate_family_invalidates_every_token(refresh_token_repo):
    await refresh_token_repo.create(
        user_id="user-1", token="tok-a", family_id="fam-1", expires_at=_future()
    )
    await refresh_token_repo.mark_rotated("tok-a", "tok-b")

    await refresh_token_repo.invalidate_family("fam-1")

    assert await refresh_token_repo.is_valid("tok-a") is False
    assert await refresh_token_repo.is_valid("tok-b") is False
