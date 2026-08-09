"""InMemoryRefreshTokenRepository (Task A.3)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict, List, Optional

from app.repositories.exceptions import ConflictError, NotFoundError
from app.repositories.models import RefreshTokenRecord


class InMemoryRefreshTokenRepository:
    def __init__(self) -> None:
        self._by_token: Dict[str, RefreshTokenRecord] = {}
        self._family_index: Dict[str, List[str]] = {}  # family_id -> [token, ...]

    async def create(
        self, user_id: str, token: str, family_id: str, expires_at: datetime
    ) -> None:
        record = RefreshTokenRecord(
            token=token, user_id=user_id, family_id=family_id, expires_at=expires_at
        )
        self._by_token[token] = record
        self._family_index.setdefault(family_id, []).append(token)

    async def get(self, token: str) -> Optional[RefreshTokenRecord]:
        return self._by_token.get(token)

    async def mark_rotated(self, old_token: str, new_token: str) -> None:
        old_record = self._by_token.get(old_token)
        if old_record is None:
            raise NotFoundError(f"No refresh token record for token={old_token!r}")
        if old_record.rotated:
            # Reuse-detection signal: someone is presenting an
            # already-rotated refresh token. The caller (B.1's service
            # layer) is expected to catch this and call
            # invalidate_family() as the theft response.
            raise ConflictError(
                f"Refresh token {old_token!r} was already rotated — possible reuse/theft."
            )
        old_record.rotated = True
        await self.create(
            user_id=old_record.user_id,
            token=new_token,
            family_id=old_record.family_id,
            expires_at=old_record.expires_at,
        )

    async def invalidate_family(self, family_id: str) -> None:
        for token in self._family_index.get(family_id, []):
            record = self._by_token.get(token)
            if record is not None:
                record.invalidated = True

    async def is_valid(self, token: str) -> bool:
        record = self._by_token.get(token)
        if record is None:
            return False
        if record.rotated or record.invalidated:
            return False
        if record.expires_at <= datetime.now(timezone.utc):
            return False
        return True
