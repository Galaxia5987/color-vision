from fastapi import FastAPI
import uvicorn

from app.lifespan.app_lifespan import app_lifespan
from app.camera.streams import router as streams_router

app = FastAPI(
    title="Color Vision",
    description="FRC Vision for color detection",
    version="0.1.0",
    lifespan=app_lifespan
)

app.include_router(streams_router, prefix="/streams")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5806)