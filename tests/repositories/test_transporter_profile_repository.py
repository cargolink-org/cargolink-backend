"""Tests for InMemoryTransporterProfileRepository (Task A.3, requirement 11)."""

import pytest

from app.repositories.exceptions import NotFoundError

pytestmark = pytest.mark.asyncio


async def test_get_by_user_id_returns_none_when_absent(transporter_profile_repo):
    result = await transporter_profile_repo.get_by_user_id("user-1")

    assert result is None


async def test_upsert_creates_profile_with_zero_rating(transporter_profile_repo):
    profile = await transporter_profile_repo.upsert(user_id="user-1", license_no="DL-123")

    assert profile.license_no == "DL-123"
    assert profile.rating_avg == 0.0


async def test_upsert_preserves_rating_avg_on_update(transporter_profile_repo):
    await transporter_profile_repo.upsert(user_id="user-1", license_no="DL-123")
    await transporter_profile_repo.update_rating_avg("user-1", 4.5)

    updated = await transporter_profile_repo.upsert(user_id="user-1", license_no="DL-456")

    assert updated.license_no == "DL-456"
    assert updated.rating_avg == 4.5  # H.2 feedback loop value must survive a profile edit


async def test_update_rating_avg_raises_not_found(transporter_profile_repo):
    with pytest.raises(NotFoundError):
        await transporter_profile_repo.update_rating_avg("no-such-user", 3.0)


async def test_update_rating_avg_updates_value(transporter_profile_repo):
    await transporter_profile_repo.upsert(user_id="user-1", license_no="DL-123")

    await transporter_profile_repo.update_rating_avg("user-1", 4.2)

    fetched = await transporter_profile_repo.get_by_user_id("user-1")
    assert fetched.rating_avg == 4.2
