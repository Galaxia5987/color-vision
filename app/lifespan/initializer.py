from pdb import run
from fastapi import FastAPI
import cv2 as cv

from app.camera import streams
from app.camera.detection_runner import DetectionRunner
from app.logging_config import get_logger
from app.camera.color_calibrator import ColorCalibrator
from app.camera.color_detector import ColorDetector
from app.config import ConfigManager
from app.utils.app_utils import generate_stream_disabled_image
from app.pipeline.pipeline_runner import PipelineRunner, PassthroughPipeline

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

        self.init_detection_runners()
        self.init_pipeline_runners()
        self.setup_stream_routes()

    def init_detection_runners(self):
        self.runners: list[DetectionRunner] = []
        for camera_config in self.config.cameras:
            lower_limit, upper_limit = camera_config.detection.limits
            min_area = camera_config.detection.min_area
            runner = DetectionRunner(
                    self.app, 
                    camera_config.name, 
                    ColorDetector(lower_limit, upper_limit, min_area)
                )
            runner.start()

            self.runners.append(
                runner
            )
        self.app.state.runners = self.runners

    def setup_stream_routes(self):
        logger.info("Configuring stream routes", operation="reload_app")

        def make_frame_source(runner: DetectionRunner, *, detection: bool):
            def frame_source():
                if not runner:
                    return DISABLED_STREAM_IMAGE

                img = (
                    runner.get_detection_jpeg()
                    if detection
                    else runner.get_mask_jpeg()
                )

                return img or DISABLED_STREAM_IMAGE

            return frame_source

        for runner in self.runners:
            streams.create_stream_route(
                self.app,
                f"/{runner.device_name}/processed",
                make_frame_source(runner, detection=True),
            )

            streams.create_stream_route(
                self.app,
                f"/{runner.device_name}/raw",
                make_frame_source(runner, detection=False),
            )

        logger.info(
            "Stream routes configured successfully",
            operation="reload_app",
            status="success",
        )

    def init_pipeline_runners(self):
        self.pipeline_runners: list[PipelineRunner] = []
        for runner in self.runners:
            pipeline_runner = PipelineRunner(
                runner.device_name,
                PassthroughPipeline(),
                runner.get_latest_frame,
            )
            pipeline_runner.start()
            self.pipeline_runners.append(pipeline_runner)
        self.app.state.pipeline_runners = self.pipeline_runners


    def stop(self):
        for pipeline_runner in getattr(self, "pipeline_runners", []):
            pipeline_runner.stop_sync()
        for runner in getattr(self, "runners", []):
            runner.stop_sync()
