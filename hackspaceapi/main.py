# -*- coding: utf-8 -*-
import logging

from fastapi import FastAPI

from .spaceapi import spaceapi


logging.basicConfig(level=logging.DEBUG)
app = FastAPI()
app.include_router(spaceapi)
