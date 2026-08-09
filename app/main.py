"""
FastAPI app skeleton (Task A.1), reconstructed here as a prerequisite for
Task A.3 — see the note at the top of app/core/enums.py.

A.3 adds exactly one thing to this file: the startup-time call to
app.core.di_registrations.register_all_repositories(), added as an
@application.on_event("startup") handler mirroring the shutdown handler
already established here, per the A.3 task prompt's requirement 7. No
other part of this file is part of A.3's scope.
"""

import socketio
from fastapi import FastAPI

from app.core.di_registrations import register_all_repositories

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

_DOMAIN_ROUTERS = [
    auth_router,
    profiles_router,
    vehicles_router,
    loads_router,
    matching_router,
    pricing_router,
    tracking_router,
    documents_router,
    checkpoints_router,
    containers_router,
    notifications_router,
    admin_router,
    ratings_router,
]


def create_app() -> FastAPI:
    application = FastAPI(
        title="CargoLink Backend",
        description="Smart Freight Matching and Tracking System — backend API.",
        version="0.1.0",
    )

    for domain_router in _DOMAIN_ROUTERS:
        application.include_router(domain_router)

    @application.on_event("startup")
    async def _startup() -> None:
        # Task A.3: populate app/core/di.py's registry with every entity's
        # (interface -> mock_factory) pair. Called here (not at import
        # time) so tests can freely call di.reset_registry() +
        # register_all_repositories() per test module without
        # import-order surprises (see A.3 requirement 7).
        register_all_repositories()

    @application.on_event("shutdown")
    async def _shutdown() -> None:
        # Placeholder for connection/resource teardown once real
        # implementations (Kishor's sqlalchemy_impl/, Sprint 5+) exist.
        pass

    return application


app = create_app()

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
# Deploy `socket_app`, not `app`, as the ASGI entrypoint (Cluster E note).
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
