import cv2
from typing import override
from app.constants import LOOP_TIME
from app.utils.async_loop_base import AsyncLoopBase
from .camera_manager import resolve_device


class WebCamera(AsyncLoopBase):
    def __init__(self, device_name: str) -> None:
        super().__init__(LOOP_TIME)
        self.device_name = device_name
        self.device_path = resolve_device(device_name)
        self.cap = cv2.VideoCapture(self.device_path)
        self._latest_frame = None

    @property
    def latest_frame(self):
        return self._latest_frame

    @override
    def on_iteration(self) -> None:
        ret, frame = self.cap.read()
        if not ret:
            return

        self._latest_frame = frame

    @override
    def on_stop(self) -> None:
        self.cap.release()