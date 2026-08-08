from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.auth.schemas import OtpRequestRequest, OtpVerifyRequest, Role, UserSummary


def test_otp_request_accepts_valid_e164_phone():
    req = OtpRequestRequest(phone="+919876543210")
    assert req.phone == "+919876543210"


@pytest.mark.parametrize("bad_phone", ["9876543210", "+91987", "not-a-phone", ""])
def test_otp_request_rejects_invalid_phone(bad_phone):
    with pytest.raises(ValidationError):
        OtpRequestRequest(phone=bad_phone)


def test_otp_verify_requires_exactly_six_digit_otp():
    OtpVerifyRequest(phone="+919876543210", otp="123456")
    with pytest.raises(ValidationError):
        OtpVerifyRequest(phone="+919876543210", otp="12345")
    with pytest.raises(ValidationError):
        OtpVerifyRequest(phone="+919876543210", otp="12345a")


def test_user_summary_never_exposes_password_hash():
    user = UserSummary(
        id=uuid4(),
        role=Role.SHIPPER,
        name="Test Shipper",
        phone="+919876543210",
        email=None,
        created_at=datetime.now(timezone.utc),
    )
    assert "password_hash" not in type(user).model_fields
    assert "otp" not in type(user).model_fields
