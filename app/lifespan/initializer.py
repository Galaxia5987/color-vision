from pdb import run
from fastapi import FastAPI
import cv2 as cv

from app.camera import streams
from app.camera.detection_runner import DetectionRunner
from app.logging_config import get_logger
from app.camera.color_calibrator import ColorCalibrator
from app.camera.color_detector import ColorDetector
from app.config import ConfigManager
from app.models.models import CameraConfig
from app.utils.app_utils import generate_stream_disabled_image
from app.pipeline.pipeline_runner import PipelineRunner, PassthroughPipeline

from app.utils.decorators import singleton

logger = get_logger(__name__)

DISABLED_STREAM_IMAGE_BYTES = (
    generate_stream_disabled_image()
) 

@singleton
class Initializer:
    def initialize(self, app: FastAPI):
        self.app = app
        self.app.state.config = ConfigManager().get()
        self.app.state.initializer = self
        self.config = self.app.state.config

        self.init_detection_runners()
        self.init_pipeline_runners()
        self.setup_stream_routes()

    def add_new_camera(self, camera_config: CameraConfig):
        runner = self.add_runner(camera_config)
        self.create_stream_routes(runner)

    def add_runner(self, camera_config: CameraConfig) -> DetectionRunner:
        lower_limit, upper_limit = camera_config.detection.limits
        min_area = camera_config.detection.min_area
        max_area = camera_config.detection.max_area
        runner = DetectionRunner(
                self.app, 
                camera_config.name, 
                ColorDetector(lower_limit, upper_limit, min_area, max_area)
            )
        runner.start()
        self.app.state.runners.append(runner)
        return runner


    def init_detection_runners(self):
        self.runners: list[DetectionRunner] = []
        self.app.state.runners = self.runners
        for camera_config in self.config.cameras:
            self.add_runner(camera_config)

    def setup_stream_routes(self):
        logger.info("Configuring stream routes", operation="reload_app")

        for runner in self.runners:
            self.create_stream_routes(runner)

        logger.info(
            "Stream routes configured successfully",
            operation="reload_app",
            status="success",
        )

    def create_stream_routes(self, runner: DetectionRunner):
        def make_frame_source(runner: DetectionRunner, *, detection: bool):
            def frame_source():
                if not runner:
                    return DISABLED_STREAM_IMAGE_BYTES

                img = (
                    runner.get_detection_jpeg()
                    if detection
                    else runner.get_mask_jpeg()
                )

                return img or DISABLED_STREAM_IMAGE_BYTES

            return frame_source
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
