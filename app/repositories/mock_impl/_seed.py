"""
Seed-loading helper for mock repositories (Task A.3, requirement 6).

Each mock implementation calls load_seed_json("<name>.json") in its
__init__ and, if a list is returned, best-effort-populates its initial
in-memory state from it. If Kishor hasn't authored shared/mock-data/ yet
(expected at this point in the project timeline — see the Execution Plan,
seed data v1 isn't shared until the Week 4 freeze), this returns None and
every mock repository must still function correctly starting empty. This
module never raises for a missing file; it only raises if the file exists
but isn't valid JSON, since that indicates a real authoring mistake worth
surfacing rather than silently swallowing.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, List, Optional

# backend/app/repositories/mock_impl/_seed.py -> repo root is 4 parents up.
_REPO_ROOT = Path(__file__).resolve().parents[4]
_MOCK_DATA_DIR = _REPO_ROOT / "shared" / "mock-data"


def load_seed_json(filename: str) -> Optional[List[dict]]:
    """Load shared/mock-data/<filename> as a list of dicts, or None if the
    file doesn't exist yet."""
    path = _MOCK_DATA_DIR / filename
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        data: Any = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON array of records")
    return data
