"""TransporterProfileRepository interface (Task A.3)."""

from typing import Optional, Protocol

from app.repositories.models import TransporterProfile


class TransporterProfileRepository(Protocol):
    async def get_by_user_id(self, user_id: str) -> Optional[TransporterProfile]:
        """Fetch a transporter's profile, or None if not yet created."""
        ...

    async def upsert(self, user_id: str, license_no: Optional[str]) -> TransporterProfile:
        """Create or update a transporter's profile."""
        ...

    async def update_rating_avg(self, user_id: str, new_avg: float) -> None:
        """H.2 feedback loop: update the transporter's rating_avg after a
        new rating is submitted, so the matching engine's scoring (C.2/C.5)
        picks up the change on the next query. Raises NotFoundError if no
        profile exists for user_id."""
        ...
