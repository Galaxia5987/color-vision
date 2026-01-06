from typing import List, Tuple, Optional
from pydantic import BaseModel

class Detection(BaseModel):
    limits: Tuple[List[int], List[int]]
    min_area: int
    max_area: int

class CameraConfig(BaseModel):
    name: str
    alias: Optional[str] = None
    detection_stream_enabled: bool
    mask_stream_enabled: bool
    detection: Detection
    exposure: int = 100

class RootConfig(BaseModel):
    cameras: List[CameraConfig]

default_config = RootConfig(
    cameras=[
        CameraConfig(
            name="someshit",
            alias=None,
            detection_stream_enabled=True,
            mask_stream_enabled=True,
            detection=Detection(
                limits=([61,48,43], [103,255,255]),
                min_area=500,
                max_area=100000
            )
        ),
    ]
)
