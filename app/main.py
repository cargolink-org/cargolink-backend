"""
CargoLink backend ASGI entrypoint.

Mounts the FastAPI REST application together with the python-socketio
real-time layer under a single ASGI app (`socket_app`), per the confirmed
technical spec (Sec 2.4):

    socket_app = socketio.ASGIApp(sio, other_asgi_app=app)

`socket_app`, not `app`, MUST be the deployed entrypoint everywhere --
local (`uvicorn app.main:socket_app`), staging, and production
(Gunicorn+Uvicorn workers). Deploying `app` alone silently breaks only the
real-time tracking layer while every REST endpoint continues to appear to
work, which is exactly the kind of bug that's expensive to catch late --
see Cluster E and Cluster I.2 in the Backend Implementation Guide.

Sprint 1 scope (Task A.1): app skeleton, global error handling, and a
minimal Socket.io mount proving the wiring works end-to-end. Full JWT
validation, room-join authorization, and location-broadcast handlers are
Task E.1 (Sprint 4) -- not implemented here.
"""
import logging
from contextlib import asynccontextmanager

import socketio
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.db import dispose_engine

logger = logging.getLogger("cargolink")
logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)


def create_app() -> FastAPI:
    """Builds and configures the FastAPI REST application (pre-Socket.io mount)."""
    application = FastAPI(
        title=settings.app_name,
        description="Smart Freight Matching & Tracking System — Backend API",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    @application.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """
        Converts any unhandled exception into CargoLink's standard error
        response shape. Never leaks a raw traceback or exception message
        to the client -- full detail goes to the server-side log only.
        """
        logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "internal_server_error",
                    "message": "An unexpected error occurred. Please try again later.",
                }
            },
        )

    @application.get("/health", tags=["system"])
    async def health() -> dict:
        """
        Liveness/health-check endpoint. Used by CI smoke tests (Task I.2)
        and, in production, by the hosting platform's health-check probe.
        Deliberately reports whether mock repositories are active, so a
        `mock_repo: true` response in a production health check is an
        instant, visible red flag.
        """
        return {
            "status": "ok",
            "environment": settings.environment.value,
            "mock_repo": settings.mock_repo,
        }

    return application


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await dispose_engine()


app = create_app()

# --- Socket.io real-time layer ---
# ASGI-mode server; wire-protocol-identical to the original Node/Socket.io
# plan, so no React Native client-side changes were needed when the
# backend language changed from Node to Python (technical spec Sec 2.4).
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
async def connect(sid: str, environ: dict, auth: dict | None) -> None:
    """
    Placeholder connect handler for Task A.1.

    Full JWT validation and room-join authorization (`load:{load_id}`)
    are implemented in Task E.1 (Sprint 4, Cluster E). This Sprint 1
    version exists only to prove the ASGI mount is wired correctly
    end-to-end; it accepts every connection unconditionally and must not
    be relied on for anything security-sensitive until E.1 lands.
    """
    logger.debug("socket connect: sid=%s", sid)


@sio.event
async def disconnect(sid: str) -> None:
    logger.debug("socket disconnect: sid=%s", sid)


# This is the ASGI entrypoint that must be deployed everywhere:
#     uvicorn app.main:socket_app
# NOT `app` on its own. See the module docstring above.
socket_app = socketio.ASGIApp(sio, other_asgi_app=app)
