# -*- coding: utf-8 -*-
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel, Field

from hackspaceapi import VERSION

from .events import events
from .spaceapi import spaceapi

logging.basicConfig(level=logging.DEBUG)
app = FastAPI(
    title="HackspaceAPI",
    description="A simple, public API for Leigh Hackspace.",
    version=VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(spaceapi)
app.include_router(events)

# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Add instrumentor for Prometheus
Instrumentator().instrument(app).expose(app)


class HealthResponse(BaseModel):
    health: str = Field(description="State of the API", examples=["ok", "error"])
    version: str = Field(description="Version of the API", examples=[VERSION])


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")


@app.get(
    "/health",
    description="Healthcheck endpoint to ensure the API is running correctly",
    tags=["Health"],
)
def health() -> HealthResponse:
    return HealthResponse(health="ok", version=VERSION)
