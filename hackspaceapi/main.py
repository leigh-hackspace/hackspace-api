# -*- coding: utf-8 -*-
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from prometheus_fastapi_instrumentator import Instrumentator

from hackspaceapi import VERSION
from hackspaceapi.models import HealthResponseModel

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

# Add instrumentor for Prometheus
Instrumentator().instrument(app).expose(app, include_in_schema=False)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")


@app.get(
    "/health",
    summary="Get API health",
    description="Healthcheck endpoint to ensure the API is running correctly",
    tags=["Health"],
)
def health() -> HealthResponseModel:
    return HealthResponseModel(health="ok", version=VERSION)
