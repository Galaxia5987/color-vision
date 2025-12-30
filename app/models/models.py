from xmlrpc.client import Boolean
from pydantic import BaseModel

class CameraConfig(BaseModel):
    usb_index: int
    detection_stream_enabled: Boolean
    mask_stream_enabled: Boolean

class Detection(BaseModel):
    limits: tuple[list[int], list[int]]

class RootConfig(BaseModel):
    camera: CameraConfig
    detection: Detection

default_config = RootConfig(
    camera = CameraConfig(
        usb_index=0,
        detection_stream_enabled=True,
        mask_stream_enabled=True
    ),
    detection=Detection(
        limits=([61,48,43], [103,255,255])
    )
)