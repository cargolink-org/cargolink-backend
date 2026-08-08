"""Export the live-generated OpenAPI spec to shared/openapi/openapi.yaml.

This is the mechanism referenced throughout the implementation guide and
by app/main.py's docstring: `shared/openapi/openapi.yaml` is not
hand-maintained, it's a committed *export* of whatever `app.openapi()`
actually produces from the Pydantic schemas + router registrations in
this codebase.

Usage:
    python -m scripts.export_openapi [--check]

    --check   Don't write the file; exit non-zero if the committed file
              would differ from what the running app generates. This is
              what backend/tests/test_openapi_contract.py effectively
              re-implements as a pytest assertion so it runs in CI
              (backend-ci.yml) without a separate script invocation step.

Known sandbox limitation: this script requires `fastapi`, `pydantic`, and
`pyyaml` to be importable. This sandbox has no network access to install
them, so this script has been written and statically checked
(py_compile / ast) but not actually executed end-to-end here — see the
implementation report for details. Run it for real in an environment
with `pip install -r backend/requirements.txt` completed.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OPENAPI_YAML_PATH = REPO_ROOT / "shared" / "openapi" / "openapi.yaml"


def generate_spec() -> dict:
    """Import the FastAPI app and return its live-generated OpenAPI dict."""
    # Imported lazily so `--help` works even without fastapi installed.
    from app.main import app  # noqa: WPS433 (intentional local import)

    return app.openapi()


def write_spec(spec: dict, path: Path = OPENAPI_YAML_PATH) -> None:
    import yaml

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(spec, fh, sort_keys=False, allow_unicode=True)


def check_spec(path: Path = OPENAPI_YAML_PATH) -> bool:
    """Return True if the committed file matches the live-generated spec."""
    import yaml

    live_spec = generate_spec()
    if not path.exists():
        return False
    committed_spec = yaml.safe_load(path.read_text(encoding="utf-8"))
    return committed_spec == live_spec


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if shared/openapi/openapi.yaml is out of sync with the running app, without writing.",
    )
    args = parser.parse_args()

    if args.check:
        in_sync = check_spec()
        if not in_sync:
            print(
                f"DRIFT DETECTED: {OPENAPI_YAML_PATH} does not match the live app.openapi() output. "
                "Run `python -m scripts.export_openapi` (without --check) and commit the result.",
                file=sys.stderr,
            )
            return 1
        print(f"OK: {OPENAPI_YAML_PATH} matches the live app.openapi() output.")
        return 0

    spec = generate_spec()
    write_spec(spec)
    print(f"Wrote {OPENAPI_YAML_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
