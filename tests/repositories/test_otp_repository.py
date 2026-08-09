"""Tests for InMemoryOtpRepository (Task A.3, requirement 11)."""

from datetime import datetime, timedelta, timezone

import pytest

from app.repositories.exceptions import NotFoundError

pytestmark = pytest.mark.asyncio


def _future(minutes=5):
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)


async def test_set_and_get(otp_repo):
    expires_at = _future()
    await otp_repo.set("+919876543210", "123456", expires_at)

    record = await otp_repo.get("+919876543210")

    assert record is not None
    assert record.code == "123456"
    assert record.expires_at == expires_at
    assert record.attempts == 0


async def test_get_returns_none_when_absent(otp_repo):
    result = await otp_repo.get("+910000000000")

    assert result is None


async def test_set_overwrites_prior_otp(otp_repo):
    await otp_repo.set("+919876543210", "111111", _future())
    await otp_repo.set("+919876543210", "222222", _future())

    record = await otp_repo.get("+919876543210")

    assert record.code == "222222"
    assert record.attempts == 0  # overwritten record starts fresh


async def test_increment_attempts(otp_repo):
    await otp_repo.set("+919876543210", "123456", _future())

    first = await otp_repo.increment_attempts("+919876543210")
    second = await otp_repo.increment_attempts("+919876543210")

    assert first == 1
    assert second == 2


async def test_increment_attempts_raises_not_found(otp_repo):
    with pytest.raises(NotFoundError):
        await otp_repo.increment_attempts("+91_never_requested")


async def test_delete_is_safe_when_absent(otp_repo):
    await otp_repo.delete("+91_never_requested")  # must not raise


async def test_delete_removes_record(otp_repo):
    await otp_repo.set("+919876543210", "123456", _future())

    await otp_repo.delete("+919876543210")

    assert await otp_repo.get("+919876543210") is None
