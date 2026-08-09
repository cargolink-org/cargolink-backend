"""RefreshTokenRepository interface.

A.3 addition — not explicitly named as an entity in
Dinesh-Backend-Implementation-Guide.md's Section 5 (its DB-table lists
never mention a `refresh_tokens` table), but B.1's confirmed requirement
—- "rotating refresh tokens... refresh token reuse after rotation (must be
detected and treated as a possible token-theft signal — invalidate the
whole token family, not just silently issue a new one)" — cannot be built
without somewhere to persist token/family state. This is the smallest
reasonable addition to satisfy that requirement; flagged here, in the A.3
task prompt, and in shared/contracts/repository-interfaces.md for Kishor's
awareness when the real schema/migration is authored.
"""

from datetime import datetime
from typing import Optional, Protocol

from app.repositories.models import RefreshTokenRecord


class RefreshTokenRepository(Protocol):
    async def create(
        self, user_id: str, token: str, family_id: str, expires_at: datetime
    ) -> None:
        """Persist a newly issued refresh token as part of a token family.
        A family groups all tokens descended from one original login, so a
        reuse-detection event can invalidate all of them at once."""
        ...

    async def get(self, token: str) -> Optional[RefreshTokenRecord]:
        """Fetch a refresh token record by its raw token value, or None if
        it doesn't exist (never issued, or already deleted)."""
        ...

    async def mark_rotated(self, old_token: str, new_token: str) -> None:
        """Mark old_token as rotated (consumed) and register new_token in
        the same family. Raises NotFoundError if old_token doesn't exist,
        ConflictError if old_token was already rotated (this second case
        is exactly the reuse-detection signal B.1 must act on)."""
        ...

    async def invalidate_family(self, family_id: str) -> None:
        """Invalidate every token in a family — the reuse-detection
        response: treat the whole family as compromised, not just the
        single reused token."""
        ...

    async def is_valid(self, token: str) -> bool:
        """True if the token exists, has not been rotated, has not been
        invalidated via its family, and has not expired."""
        ...
