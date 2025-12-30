from app.constants import LOOP_TIME
from app.utils.async_loop_base import AsyncLoopBase


class PipelineRunner(AsyncLoopBase):

    def __init__(self):
        super().__init__(LOOP_TIME)
    

    def on_iteration(self):
        pass