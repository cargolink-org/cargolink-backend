"""InMemoryFareQuoteRepository (Task A.3)."""

from __future__ import annotations

from typing import Dict, Optional

from app.repositories.models import FareQuote, new_id


class InMemoryFareQuoteRepository:
    def __init__(self) -> None:
        self._by_id: Dict[str, FareQuote] = {}
        self._latest_by_load: Dict[str, str] = {}  # load_id -> quote id

    async def create(
        self, load_id: str, base_fare: float, distance_cost: float, surcharge: float, total: float
    ) -> FareQuote:
        quote = FareQuote(
            id=new_id(),
            load_id=load_id,
            base_fare=base_fare,
            distance_cost=distance_cost,
            surcharge=surcharge,
            total=total,
        )
        self._by_id[quote.id] = quote
        self._latest_by_load[load_id] = quote.id  # a fresh quote supersedes the prior one
        return quote

    async def get_by_load(self, load_id: str) -> Optional[FareQuote]:
        quote_id = self._latest_by_load.get(load_id)
        return self._by_id.get(quote_id) if quote_id else None
