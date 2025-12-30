
from cv2 import VideoCapture
from app.camera.color_detector import ColorDetector
from app.config import ConfigManager
from app.logging_config import get_logger
from app.utils.async_loop_base import AsyncLoopBase

LOOP_INTERVAL = 0.01 # 100 Hz

logger = get_logger(__name__)

class DetectionRunner(AsyncLoopBase):
    def __init__(self, app):
        super().__init__(LOOP_INTERVAL)

        self.app = app
        self.camera: VideoCapture = self.app.state.camera
        self.detector: ColorDetector = self.app.state.detector

    def on_iteration(self):
        ret, frame = self.camera.read()

        logger.info(f"Frame: {frame}")

        self.detector.proccess(frame)
        
    def get_detection_jpeg(self):
        if ConfigManager().get().camera.detection_stream_enabled:
            return self.detector.get_detections_jpeg()
        return None
    
    def get_mask_jpeg(self):
        if ConfigManager().get().camera.mask_stream_enabled:
            return self.detector.get_masked_frame()
        return None