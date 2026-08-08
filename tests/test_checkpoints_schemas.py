from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.checkpoints.schemas import CheckpointCreateRequest, CheckpointName, CheckpointStatus


def test_checkpoint_name_has_exactly_five_defined_stages():
    assert {c.value for c in CheckpointName} == {
        "origin_warehouse",
        "port_border",
        "customs_hold",
        "cleared",
        "destination",
    }


def test_checkpoint_create_accepts_every_defined_stage():
    for name in CheckpointName:
        CheckpointCreateRequest(checkpoint_name=name, status=CheckpointStatus.COMPLETE)


def test_checkpoint_create_rejects_unknown_stage():
    with pytest.raises(ValidationError):
        CheckpointCreateRequest(checkpoint_name="mid_ocean", status=CheckpointStatus.COMPLETE)
