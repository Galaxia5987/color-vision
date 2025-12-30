from fastapi import FastAPI
import cv2 as cv

from app.camera import streams
from app.camera.detection_runner import DetectionRunner
from app.logging_config import get_logger
from app.camera.color_calibrator import ColorCalibrator
from app.camera.color_detector import ColorDetector
from app.config import ConfigManager
from app.utils.app_utils import generate_stream_disabled_image

from app.utils.decorators import singleton

logger = get_logger(__name__)

DISABLED_STREAM_IMAGE = (
    generate_stream_disabled_image()
) 

@singleton
class Initializer:
    def initialize(self, app: FastAPI):
        self.app = app
        self.app.state.config = ConfigManager().get()
        self.config = self.app.state.config

        self.init_detector()
        self.init_detection_runner()

        # self.init_calibrator()
        
        self.setup_stream_routes()

    def init_calibrator(self):
        self.calibrator = ColorCalibrator(self.app.state.camera)

    def init_detector(self):
        limits_config = self.app.state.config.detection.limits
        lower_limit = limits_config[0]
        upper_limit = limits_config[1] 
        self.app.state.detector = ColorDetector(lower_limit, upper_limit)

    def init_detection_runner(self):
        self.runner = DetectionRunner(self.app, )
        self.app.state.runner = self.runner
        

    def setup_stream_routes(self):
        logger.info("Configuring stream routes", operation="reload_app")

        def video(detection: bool):
            if not self.runner:
                return DISABLED_STREAM_IMAGE
            img = None
            if detection:
                img = self.runner.get_detection_jpeg()
            else:
                img = self.runner.get_mask_jpeg()
            if img is None:
                return DISABLED_STREAM_IMAGE
            return img

        def video_detections():
            return video(False)

        def video_masked():
            return video(True)

        streams.create_stream_route(self.app, "/detections_feed", video_detections)
        streams.create_stream_route(self.app, "/masked_feed", video_masked)

        logger.info(
            "Stream routes configured successfully",
            operation="reload_app",
            status="success",
        )

    def stop(self):
        pass