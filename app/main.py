"""CargoLink FastAPI application entrypoint.

Exposes:
  - `app`         the FastAPI instance (title="CargoLink Backend").
  - `socket_app`  the combined ASGI app (FastAPI + python-socketio), the
                   actual deployment entrypoint per the technical spec's
                   §2.4 integration pattern. Full `python-socketio`
                   handlers are Task E.1's job — this file only mounts an
                   inert AsyncServer so the ASGI wrapper exists, matching
                   the Sprint 1 "Socket.io ASGI mount scaffold" deliverable.

Treated as pre-existing per A.1 (not found in this sandbox, recreated
minimally with the exact global-exception-handler shape the A.2 task
description specifies, so downstream code has something real to import).

A.2 additions: registration of every domain router below so FastAPI's
OpenAPI generation (`app.openapi()`, `/openapi.json`, `/docs`, `/redoc`)
reflects the full contract. No business logic is added here — every
handler in every domain router is a stub.
"""
from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.errors import ErrorDetail, ErrorResponse

logger = logging.getLogger("cargolink.backend")


def create_app() -> FastAPI:
    application = FastAPI(
        title="CargoLink Backend",
        description=(
            "Smart Freight Matching & Tracking System — backend API. "
            "This is the live-generated source of truth for the API contract; "
            "the committed, versioned export lives at shared/openapi/openapi.yaml "
            "and is checked for drift by backend/tests/test_openapi_contract.py."
        ),
        version="0.1.0",
    )

    @application.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error=ErrorDetail(code="internal_error", message="An unexpected error occurred.")
            ).model_dump(),
        )

    # --- Domain routers -------------------------------------------------
    # Registered here purely so /openapi.json reflects the full A.2
    # contract. Handler bodies are NotImplementedError stubs; B.1 onward
    # fills in real business logic per-domain.
    from app.admin.router import router as admin_router
    from app.auth.router import router as auth_router
    from app.checkpoints.router import router as checkpoints_router
    from app.containers.router import router as containers_router
    from app.documents.router import router as documents_router
    from app.loads.router import router as loads_router
    from app.matching.router import router as matching_router
    from app.notifications.router import router as notifications_router
    from app.pricing.router import router as pricing_router
    from app.profiles.router import router as profiles_router
    from app.ratings.router import router as ratings_router
    from app.tracking.router import router as tracking_router
    from app.vehicles.router import router as vehicles_router

    application.include_router(auth_router)
    application.include_router(profiles_router)
    application.include_router(vehicles_router)
    application.include_router(loads_router)
    application.include_router(matching_router)
    application.include_router(pricing_router)
    application.include_router(tracking_router)
    application.include_router(documents_router)
    application.include_router(checkpoints_router)
    application.include_router(containers_router)
    application.include_router(notifications_router)
    application.include_router(admin_router)
    application.include_router(ratings_router)

    return application


app = create_app()

# --- Socket.io ASGI mount (scaffold only; full handlers are Task E.1) ----
try:
    import socketio

    sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
    socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
except ImportError:  # pragma: no cover - python-socketio not installed in this sandbox
    sio = None
    socket_app = app
