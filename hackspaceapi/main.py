# -*- coding: utf-8 -*-
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from prometheus_fastapi_instrumentator import Instrumentator

from hackspaceapi import VERSION

from .events import events
from .spaceapi import spaceapi
from .doors import doors

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
app.include_router(doors, prefix='/doors')

# Add prometheus asgi middleware to route /metrics requests
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Add instrumentor for Prometheus
Instrumentator().instrument(app).expose(app)

@app.get(
    "/health",
    description="Healthcheck endpoint to ensure the API is running correctly",
    tags=["Health"],
)
def health():
    return {"health": "ok", "version": VERSION}
