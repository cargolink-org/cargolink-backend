"""OtpRepository interface (Task A.3). Consumed by B.1's OTP request/verify
lifecycle, including expiry and lockout-after-N-failures handling."""

from datetime import datetime
from typing import Optional, Protocol

from app.repositories.models import OtpRecord


class OtpRepository(Protocol):
    async def set(self, phone: str, code: str, expires_at: datetime) -> None:
        """Store a freshly generated OTP for a phone number, overwriting
        any prior (unexpired or expired) OTP for that same phone — a new
        OTP request always supersedes the previous one."""
        ...

    async def get(self, phone: str) -> Optional[OtpRecord]:
        """Fetch the current OTP record for a phone number, or None if
        none has been requested (or it was already consumed/deleted)."""
        ...

    async def increment_attempts(self, phone: str) -> int:
        """Increment and return the failed-verify attempt counter for a
        phone's current OTP (B.1 lockout-after-N-failures). Raises
        NotFoundError if no OTP record exists for the phone."""
        ...

    async def delete(self, phone: str) -> None:
        """Remove the OTP record for a phone number (post successful
        verify, or on expiry cleanup). Safe to call if none exists."""
        ...
