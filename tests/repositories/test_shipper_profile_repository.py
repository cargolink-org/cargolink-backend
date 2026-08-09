"""Tests for InMemoryShipperProfileRepository (Task A.3, requirement 11)."""

import pytest

pytestmark = pytest.mark.asyncio


async def test_get_by_user_id_returns_none_when_absent(shipper_profile_repo):
    result = await shipper_profile_repo.get_by_user_id("user-1")

    assert result is None


async def test_upsert_creates_profile(shipper_profile_repo):
    profile = await shipper_profile_repo.upsert(
        user_id="user-1", company_name="Acme Exports", gstin="27ABCDE1234F1Z5"
    )

    assert profile.user_id == "user-1"
    assert profile.company_name == "Acme Exports"
    assert profile.gstin == "27ABCDE1234F1Z5"

    fetched = await shipper_profile_repo.get_by_user_id("user-1")
    assert fetched == profile


async def test_upsert_without_gstin_is_optional(shipper_profile_repo):
    profile = await shipper_profile_repo.upsert(
        user_id="user-1", company_name="Solo Trader", gstin=None
    )

    assert profile.gstin is None


async def test_upsert_updates_existing_profile(shipper_profile_repo):
    await shipper_profile_repo.upsert(user_id="user-1", company_name="Old Name", gstin=None)

    updated = await shipper_profile_repo.upsert(
        user_id="user-1", company_name="New Name", gstin="27ABCDE1234F1Z5"
    )

    assert updated.company_name == "New Name"
    fetched = await shipper_profile_repo.get_by_user_id("user-1")
    assert fetched.company_name == "New Name"
