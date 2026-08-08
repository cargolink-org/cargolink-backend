from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.containers.schemas import ContainerCreateRequest, ContainerUpdateRequest


def _valid_kwargs(**overrides):
    kwargs = dict(
        container_no="MSCU1234567",
        vessel_or_flight="MSC Anna",
        port_of_loading="Nhava Sheva (INNSA)",
        port_of_discharge="Jebel Ali (AEJEA)",
    )
    kwargs.update(overrides)
    return kwargs


def test_container_create_accepts_valid_iso6346_number():
    req = ContainerCreateRequest(**_valid_kwargs())
    assert req.container_no == "MSCU1234567"


@pytest.mark.parametrize("bad_no", ["mscu1234567", "MSCU123456", "MSC1234567A", "1234567MSCU"])
def test_container_create_rejects_malformed_container_number(bad_no):
    with pytest.raises(ValidationError):
        ContainerCreateRequest(**_valid_kwargs(container_no=bad_no))


def test_container_update_allows_all_fields_optional():
    update = ContainerUpdateRequest()
    assert update.container_no is None
    assert update.vessel_or_flight is None
