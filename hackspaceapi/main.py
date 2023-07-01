# -*- coding: utf-8 -*-
import logging

from fastapi import FastAPI

from .events import events
from .spaceapi import spaceapi

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

app.include_router(spaceapi)
app.include_router(events)


@app.get("/health")
def health():
    return {"health": "ok"}
