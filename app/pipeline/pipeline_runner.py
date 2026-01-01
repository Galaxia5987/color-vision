from typing import Any, Callable

from app.constants import LOOP_TIME
from app.logging_config import get_logger
from app.pipeline.pipeline_base import CVPipeline
from app.utils.async_loop_base import AsyncLoopBase


class PipelineRunner(AsyncLoopBase):

    def __init__(self, name: str, pipeline: CVPipeline, frame_source: Callable[[], Any]):
        super().__init__(LOOP_TIME)
        self.name = name
        self.pipeline = pipeline
        self.frame_source = frame_source
        self.logger = get_logger(__name__)

    def on_iteration(self):
        frame = self.frame_source()
        if frame is None:
            return

        self.pipeline.process(frame)
        self.pipeline.publish()

    def on_stop(self) -> None:
        self.logger.info(
            f"Pipeline runner stopped: {self.name}",
            operation="pipeline_runner",
        )


class PassthroughPipeline(CVPipeline):
    def __init__(self) -> None:
        super().__init__()

    def process(self, frame: Any) -> None:
        self._output_image = frame
        self._output_data = None

    def publish(self) -> None:
        return None

    @property
    def output_image(self) -> Any:
        return self._output_image

    @property
    def output(self) -> Any:
        return self._output_data
