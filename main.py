from fastapi import FastAPI
import uvicorn

from app.lifespan.app_lifespan import app_lifespan
from app.camera.streams import router as streams_router
from app.api.router import router as api_router
from app.utils.app_utils import mount_frontend

app = FastAPI(
    title="Color Vision",
    description="FRC Vision for color detection",
    version="0.1.0",
    lifespan=app_lifespan
)

app.include_router(streams_router)
app.include_router(api_router)
mount_frontend(app)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5806)
