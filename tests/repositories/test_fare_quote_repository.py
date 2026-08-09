"""Tests for InMemoryFareQuoteRepository (Task A.3, requirement 11)."""

import pytest

pytestmark = pytest.mark.asyncio


async def test_get_by_load_returns_none_when_absent(fare_quote_repo):
    result = await fare_quote_repo.get_by_load("load-1")

    assert result is None


async def test_create_and_get_by_load(fare_quote_repo):
    quote = await fare_quote_repo.create(
        load_id="load-1", base_fare=500.0, distance_cost=1200.0, surcharge=100.0, total=1800.0
    )

    fetched = await fare_quote_repo.get_by_load("load-1")

    assert fetched.id == quote.id
    assert fetched.total == 1800.0


async def test_create_again_supersedes_prior_quote(fare_quote_repo):
    await fare_quote_repo.create(
        load_id="load-1", base_fare=500.0, distance_cost=1200.0, surcharge=100.0, total=1800.0
    )
    newer = await fare_quote_repo.create(
        load_id="load-1", base_fare=500.0, distance_cost=1400.0, surcharge=100.0, total=2000.0
    )

    fetched = await fare_quote_repo.get_by_load("load-1")

    assert fetched.id == newer.id
    assert fetched.total == 2000.0
