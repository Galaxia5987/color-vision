
from typing import override
from cv2 import VideoCapture
import cv2
from app.camera.color_detector import ColorDetector
from app.config import ConfigManager
from app.constants import LOOP_TIME
from app.logging_config import get_logger
from app.utils.async_loop_base import AsyncLoopBase
from app.utils.device_utils import resolve_device

logger = get_logger(__name__)

class DetectionRunner(AsyncLoopBase):
    def __init__(self, app, device_name: str):
        super().__init__(LOOP_TIME)

        self.device_name = device_name
        self.device_path = resolve_device(device_name)
        self.cap = cv2.VideoCapture(self.device_path)

        self.detector: ColorDetector = self.app.state.detector
        self.app = app
    
    @override
    def on_iteration(self):
        ret, frame = self.cap.read()

        if not ret:
            return

        self.detector.proccess(frame)

    def get_detection_jpeg(self):
        if ConfigManager().get().camera.detection_stream_enabled:
            return self.detector.get_detections_jpeg()
        return None
    
    def get_mask_jpeg(self):
        if ConfigManager().get().camera.mask_stream_enabled:
            return self.detector.get_masked_frame()
        return None
    
    @override
    def on_stop(self) -> None:
        self.cap.release()