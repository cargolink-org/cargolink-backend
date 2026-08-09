"""InMemoryOtpRepository (Task A.3)."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from app.repositories.exceptions import NotFoundError
from app.repositories.models import OtpRecord


class InMemoryOtpRepository:
    def __init__(self) -> None:
        self._by_phone: Dict[str, OtpRecord] = {}
        # OTPs are never seeded from shared/mock-data — they're short-lived
        # and generated at runtime, never fixture data.

    async def set(self, phone: str, code: str, expires_at: datetime) -> None:
        # Overwrites any prior OTP for this phone, per the interface contract.
        self._by_phone[phone] = OtpRecord(phone=phone, code=code, expires_at=expires_at, attempts=0)

    async def get(self, phone: str) -> Optional[OtpRecord]:
        return self._by_phone.get(phone)

    async def increment_attempts(self, phone: str) -> int:
        record = self._by_phone.get(phone)
        if record is None:
            raise NotFoundError(f"No OTP record for phone={phone!r}")
        record.attempts += 1
        return record.attempts

    async def delete(self, phone: str) -> None:
        self._by_phone.pop(phone, None)
