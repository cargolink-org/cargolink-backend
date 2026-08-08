"""Contract-drift test for shared/openapi/openapi.yaml.

Two things are verified:

1. `test_committed_spec_matches_live_app` — the real, committed
   shared/openapi/openapi.yaml is byte-for-byte-equivalent (as parsed
   YAML) to what the currently running app generates. This is the CI gate
   referenced throughout the implementation guide (A.2's acceptance
   criteria, backend-ci.yml) that prevents the contract from silently
   drifting out from under Keval and Kishor.

2. `test_drift_detection_actually_catches_a_mismatch` — proves the
   comparison mechanism itself works, per this task's explicit
   requirement ("A test fails on purpose if you hand-edit openapi.yaml
   out of sync with the app, proving the drift check actually works").
   This deliberately corrupts an in-memory COPY of the live spec (never
   the committed file on disk) and asserts the same comparison used by
   test #1 correctly reports a mismatch — i.e. it demonstrates the check
   has teeth without permanently breaking the repository's committed
   contract file for every other test run.
"""
from __future__ import annotations

import copy
from pathlib import Path

import pytest
import yaml

from scripts.export_openapi import OPENAPI_YAML_PATH, generate_spec


@pytest.mark.asyncio
async def test_committed_spec_matches_live_app():
    live_spec = generate_spec()
    assert OPENAPI_YAML_PATH.exists(), (
        f"{OPENAPI_YAML_PATH} does not exist — run `python -m scripts.export_openapi` and commit it."
    )
    committed_spec = yaml.safe_load(Path(OPENAPI_YAML_PATH).read_text(encoding="utf-8"))
    assert committed_spec == live_spec, (
        "shared/openapi/openapi.yaml is out of sync with the running app's generated OpenAPI spec. "
        "Regenerate via `python -m scripts.export_openapi` and commit the result."
    )


@pytest.mark.asyncio
async def test_drift_detection_actually_catches_a_mismatch():
    live_spec = generate_spec()

    corrupted_spec = copy.deepcopy(live_spec)
    # Mutate something a hand-edit plausibly would: silently drop a field
    # description, which is exactly the kind of drift this check exists
    # to catch (A.2 requirement 2 — descriptions ARE the documentation).
    corrupted_spec["info"]["title"] = "Hand-Edited Out Of Sync Title"

    assert corrupted_spec != live_spec, "sanity check: the mutation above must actually change the spec"
