
import logging
from typing import override
from cv2 import VideoCapture
import cv2
from app.camera.color_detector import ColorDetector
from app.config import ConfigManager
from app.constants import LOOP_TIME
from app.logging_config import get_logger
from app.models.models import CameraConfig
from app.utils.app_utils import get_camera_config_by_name
from app.utils.async_loop_base import AsyncLoopBase
from app.utils.device_utils import resolve_device, set_auto_exposure
import platform

logger = get_logger(__name__)

class DetectionRunner(AsyncLoopBase):
    def __init__(self, app, device_name: str, detector: ColorDetector):
        super().__init__(LOOP_TIME)
        
        self.device_name = device_name

        if platform.system() == "Windows":
            logging.warning("\nUSING SETTINGS FOR WINDOWS DEVELOPMENT!\n")
            self.cap = cv2.VideoCapture(0)
        else:
            self.device_path = resolve_device(device_name)
            self.cap = cv2.VideoCapture(self.device_path)
            # set_auto_exposure(self.device_path, False)
            
        
        self.camera_config: CameraConfig = get_camera_config_by_name(device_name)
        self.detector = detector
        self.app = app
        self._apply_exposure(self.camera_config.exposure)

    def _apply_exposure(self, exposure: int) -> bool:
        """Apply exposure setting to camera."""
        if self.cap is None or not self.cap.isOpened():
            logger.error("Cannot apply exposure: camera not initialized")
            return False
    
        # Apply exposure value directly.
        applied = self.cap.set(cv2.CAP_PROP_EXPOSURE, float(exposure))
        logging.info(f"Applying exposure {exposure}")
        if not applied:
            logger.warning(
                "Camera exposure update rejected by driver",
                extra={"exposure": exposure, "device": self.device_name}
            )
        
        return applied

    def update_exposure(self, exposure: int) -> bool:
        """Update camera exposure setting."""
        self.camera_config.exposure = exposure
        return self._apply_exposure(exposure)
    
    @override
    def on_iteration(self):
        ret, frame = self.cap.read()

        if not ret:
            return

        self.detector.proccess(frame)

    def get_detection_jpeg(self):
        if self.camera_config.detection_stream_enabled:
            return self.detector.get_detections_jpeg()
        return None
    
    def get_mask_jpeg(self):
        if self.camera_config.mask_stream_enabled:
            return self.detector.get_masked_frame()
        return None

    def get_latest_frame(self):
        return self.detector.latest_frame
    
    @override
    def on_stop(self) -> None:
        self.cap.release()
