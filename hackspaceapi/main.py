# -*- coding: utf-8 -*-
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get(
    "/health",
    description="Healthcheck endpoint to ensure the API is running correctly",
    tags=["Health"],
)
def health():
    return {"health": "ok"}
