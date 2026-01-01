import numpy as np
from fastapi import APIRouter, Body, HTTPException, Request

from app.config import ConfigManager, ConfigError
from app.models.models import RootConfig, CameraConfig


router = APIRouter(prefix="/api")

def _get_camera_config(config: RootConfig, name: str) -> CameraConfig | None:
    return next((cam for cam in config.cameras if cam.name == name), None)


def _get_runner(app, name: str):
    runners = getattr(app.state, "runners", None) or []
    return next((runner for runner in runners if runner.device_name == name), None)


@router.get("/config")
async def get_config() -> dict:
    return ConfigManager().get().model_dump()


@router.get("/cameras")
async def list_cameras() -> dict:
    config = ConfigManager().get()
    return {"cameras": [cam.model_dump() for cam in config.cameras]}


@router.patch("/cameras/{camera_name}")
async def update_camera_settings(
    camera_name: str, update: CameraConfig, request: Request
) -> dict:
    config = ConfigManager().get()
    camera_config = _get_camera_config(config, camera_name)

    if camera_config is None:
        raise HTTPException(status_code=404, detail="Camera not found")

    if update.name != camera_name:
        raise HTTPException(
            status_code=400, detail="Camera name in body must match URL"
        )

    camera_config.detection_stream_enabled = update.detection_stream_enabled
    camera_config.mask_stream_enabled = update.mask_stream_enabled
    camera_config.exposure = update.exposure
    camera_config.detection.limits = update.detection.limits
    camera_config.detection.min_area = update.detection.min_area

    runner = _get_runner(request.app, camera_name)
    runner_active = runner is not None
    if runner_active:
        runner.camera_config = camera_config
        lower, upper = update.detection.limits
        runner.detector.lower = np.array(lower)
        runner.detector.upper = np.array(upper)
        runner.detector.min_area = update.detection.min_area

    request.app.state.config = config

    return {
        "camera": camera_config.model_dump(),
        "runner_active": runner_active,
    }


@router.post("/config/save")
async def save_config(
    request: Request,
    config: RootConfig | None = Body(default=None),
) -> dict:
    manager = ConfigManager()
    if config is None:
        config = manager.get()
    manager.update(config)
    request.app.state.config = config
    return {"status": "saved", "path": str(manager.path)}


@router.post("/config/reload")
async def reload_config(request: Request) -> dict:
    manager = ConfigManager()
    try:
        config = manager.reload()
    except ConfigError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    request.app.state.config = config
    return {"status": "reloaded", "config": config.model_dump()}
