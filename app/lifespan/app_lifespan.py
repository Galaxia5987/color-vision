from contextlib import asynccontextmanager
from fastapi import FastAPI
from .initializer import Initializer


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    Initializer().initialize(app)
    yield
    Initializer().stop()