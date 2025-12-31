from pathlib import Path
import cv2
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import numpy as np

from app.config import ConfigManager
from app.models.models import CameraConfig


def mount_frontend(app: FastAPI) -> None:
    """Mount the built Vue frontend if available."""

    backend_dir = Path(__file__).resolve().parent
    dist_dir = (backend_dir.parent.parent / "frontend" / "dist").resolve()
    index_html = dist_dir / "index.html"

    if dist_dir.exists() and index_html.exists():
        # Serve static assets
        app.mount(
            "/assets",
            StaticFiles(directory=dist_dir / "assets"),
            name="assets",
        )

        # Catch-all route for Vue Router (history mode)
        @app.get("/{full_path:path}")
        async def serve_vue_app(full_path: str):
            return FileResponse(index_html)

    else:

        @app.get("/{full_path:path}")
        async def missing_frontend(full_path: str) -> JSONResponse:
            return JSONResponse(
                {
                    "message": (
                        f"Frontend build not found at {dist_dir}. "
                        "Run `npm run build` inside frontend."
                    )
                },
                status_code=200,
            )

def generate_stream_disabled_image(width=640, height=480, text="Stream Disabled"):
    image = np.zeros((height, width, 3), dtype=np.uint8)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    font_color = (255, 255, 255)  # white
    thickness = 2

    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_width, text_height = text_size

    x = (width - text_width) // 2
    y = (height + text_height) // 2

    cv2.putText(
        image,
        text,
        (x, y),
        font,
        font_scale,
        font_color,
        thickness,
        lineType=cv2.LINE_AA,
    )

    return image

def get_camera_config_by_name(name: str) -> CameraConfig:
    for cam in ConfigManager().get().cameras:
        if cam.name == name:
            return cam

    raise KeyError(f"Camera config with name '{name}' not found")

    
