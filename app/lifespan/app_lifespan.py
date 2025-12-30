from contextlib import asynccontextmanager
from fastapi import FastAPI
from .initializer import Initializer
from app.utils.app_utils import mount_frontend


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    Initializer().initialize(app)
    mount_frontend(app)
    yield
    Initializer().stop()