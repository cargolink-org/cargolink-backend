"""Tests for InMemoryCheckpointUpdateRepository (Task A.3, requirement 11)."""

import pytest

from app.core.enums import CheckpointName, CheckpointStatus

pytestmark = pytest.mark.asyncio


async def test_get_last_returns_none_when_no_updates(checkpoint_update_repo):
    result = await checkpoint_update_repo.get_last("load-1")

    assert result is None


async def test_create_and_list_by_load(checkpoint_update_repo):
    update = await checkpoint_update_repo.create(
        load_id="load-1",
        checkpoint_name=CheckpointName.ORIGIN_WAREHOUSE,
        status=CheckpointStatus.REACHED,
        posted_by="user-transporter-1",
        out_of_sequence=False,
    )

    updates = await checkpoint_update_repo.list_by_load("load-1")

    assert updates == [update]
    assert update.posted_by == "user-transporter-1"  # audit-log field present


async def test_list_by_load_sorted_by_timestamp(checkpoint_update_repo):
    first = await checkpoint_update_repo.create(
        load_id="load-1", checkpoint_name=CheckpointName.ORIGIN_WAREHOUSE,
        status=CheckpointStatus.REACHED, posted_by="u1", out_of_sequence=False,
    )
    second = await checkpoint_update_repo.create(
        load_id="load-1", checkpoint_name=CheckpointName.PORT_OR_BORDER,
        status=CheckpointStatus.REACHED, posted_by="u1", out_of_sequence=False,
    )

    updates = await checkpoint_update_repo.list_by_load("load-1")

    assert [u.id for u in updates] == [first.id, second.id]


async def test_get_last_returns_most_recent(checkpoint_update_repo):
    await checkpoint_update_repo.create(
        load_id="load-1", checkpoint_name=CheckpointName.ORIGIN_WAREHOUSE,
        status=CheckpointStatus.REACHED, posted_by="u1", out_of_sequence=False,
    )
    second = await checkpoint_update_repo.create(
        load_id="load-1", checkpoint_name=CheckpointName.PORT_OR_BORDER,
        status=CheckpointStatus.REACHED, posted_by="u1", out_of_sequence=False,
    )

    last = await checkpoint_update_repo.get_last("load-1")

    assert last.id == second.id


async def test_create_records_out_of_sequence_flag(checkpoint_update_repo):
    update = await checkpoint_update_repo.create(
        load_id="load-1", checkpoint_name=CheckpointName.CLEARED,
        status=CheckpointStatus.REACHED, posted_by="u1", out_of_sequence=True,
    )

    assert update.out_of_sequence is True


async def test_list_by_load_only_returns_matching_load(checkpoint_update_repo):
    await checkpoint_update_repo.create(
        load_id="load-1", checkpoint_name=CheckpointName.ORIGIN_WAREHOUSE,
        status=CheckpointStatus.REACHED, posted_by="u1", out_of_sequence=False,
    )
    await checkpoint_update_repo.create(
        load_id="load-2", checkpoint_name=CheckpointName.ORIGIN_WAREHOUSE,
        status=CheckpointStatus.REACHED, posted_by="u1", out_of_sequence=False,
    )

    updates = await checkpoint_update_repo.list_by_load("load-1")

    assert len(updates) == 1
    assert updates[0].load_id == "load-1"
