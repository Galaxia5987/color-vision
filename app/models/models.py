from typing import List, Tuple
from pydantic import BaseModel

class Detection(BaseModel):
    limits: Tuple[List[int], List[int]]

class CameraConfig(BaseModel):
    name: str
    detection_stream_enabled: bool
    mask_stream_enabled: bool
    detection: Detection

class RootConfig(BaseModel):
    cameras: List[CameraConfig]

default_config = RootConfig(
    cameras=[
        CameraConfig(
            name="someshit",
            detection_stream_enabled=True,
            mask_stream_enabled=True,
            detection=Detection(limits=([61,48,43], [103,255,255]))
        ),
    ]
)
