"""Tests for InMemoryUserRepository (Task A.3, requirement 11)."""

import pytest

from app.core.enums import UserRole
from app.repositories.exceptions import ConflictError, NotFoundError


pytestmark = pytest.mark.asyncio


async def test_create_and_get_by_id(user_repo):
    user = await user_repo.create(phone="+919876543210", role=UserRole.SHIPPER)

    fetched = await user_repo.get_by_id(user.id)

    assert fetched.id == user.id
    assert fetched.phone == "+919876543210"
    assert fetched.role == UserRole.SHIPPER


async def test_get_by_id_raises_not_found(user_repo):
    with pytest.raises(NotFoundError):
        await user_repo.get_by_id("does-not-exist")


async def test_get_by_phone_returns_none_when_unregistered(user_repo):
    result = await user_repo.get_by_phone("+910000000000")

    assert result is None


async def test_get_by_phone_returns_user_after_create(user_repo):
    created = await user_repo.create(phone="+919876543211", role=UserRole.TRANSPORTER)

    fetched = await user_repo.get_by_phone("+919876543211")

    assert fetched is not None
    assert fetched.id == created.id


async def test_create_raises_conflict_on_duplicate_phone(user_repo):
    await user_repo.create(phone="+919876543212", role=UserRole.SHIPPER)

    with pytest.raises(ConflictError):
        await user_repo.create(phone="+919876543212", role=UserRole.TRANSPORTER)


async def test_exists(user_repo):
    user = await user_repo.create(phone="+919876543213", role=UserRole.ADMIN)

    assert await user_repo.exists(user.id) is True
    assert await user_repo.exists("some-other-id") is False
