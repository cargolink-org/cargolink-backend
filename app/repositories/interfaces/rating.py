"""RatingRepository interface (Task A.3)."""

from typing import List, Optional, Protocol

from app.repositories.models import Rating


class RatingRepository(Protocol):
    async def create(
        self, load_id: str, rater_id: str, ratee_id: str, score: int, comment: Optional[str]
    ) -> Rating:
        """Submit a post-trip rating. Raises ConflictError on a duplicate
        (load_id, rater_id, ratee_id) triple (H.2's server-side
        duplicate-submission guard — must be enforced here, not just
        client-side, per A.3 requirement 5)."""
        ...

    async def exists(self, load_id: str, rater_id: str, ratee_id: str) -> bool:
        """H.2 duplicate check, usable by service.py before attempting
        create() for a friendlier error path than catching ConflictError."""
        ...

    async def list_for_ratee(self, ratee_id: str) -> List[Rating]:
        """H.2 rating_avg recompute: every rating ever received by a
        ratee, used to compute (or incrementally update) rating_avg."""
        ...
