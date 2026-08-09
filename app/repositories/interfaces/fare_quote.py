"""FareQuoteRepository interface (Task A.3)."""

from typing import Optional, Protocol

from app.repositories.models import FareQuote


class FareQuoteRepository(Protocol):
    async def create(
        self,
        load_id: str,
        base_fare: float,
        distance_cost: float,
        surcharge: float,
        total: float,
    ) -> FareQuote:
        """Persist a computed fare quote (D.1's rule-based formula
        output)."""
        ...

    async def get_by_load(self, load_id: str) -> Optional[FareQuote]:
        """Fetch the most recent fare quote for a load, or None if no
        quote has been generated yet."""
        ...
