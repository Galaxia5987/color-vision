from abc import ABC, abstractmethod
from typing import Any


class CVPipeline(ABC):
    """
    Single-process computer vision pipeline.
    Runs, stores results, and publishes them.
    """

    def __init__(self) -> None:
        self._output_image: Any | None = None
        self._output_data: Any | None = None

    @abstractmethod
    def process(self, frame: Any) -> None:
        """
        Implement the full pipeline logic.
        Must set internal outputs.
        """
        raise NotImplementedError()

    @abstractmethod
    def publish(self) -> None:
        """
        Publish pipeline results.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def output_image(self) -> Any:
        """
        Image output for visualization or streaming.
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def output(self) -> Any:
        """
        General structured output from the pipeline.
        """
        raise NotImplementedError()
