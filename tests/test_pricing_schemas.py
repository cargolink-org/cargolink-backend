from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.pricing.schemas import PricingQuoteResponse


def test_pricing_quote_rejects_negative_components():
    with pytest.raises(ValidationError):
        PricingQuoteResponse(base_fare=-1, distance_cost=10, surcharge=0, total=9)


def test_pricing_quote_accepts_zero_surcharge():
    quote = PricingQuoteResponse(base_fare=500, distance_cost=250, surcharge=0, total=750)
    assert quote.total == 750
