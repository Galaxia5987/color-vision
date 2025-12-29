from fastapi import FastAPI

from ..utils.decorators import singleton

@singleton
class Initializer:

    def initialize(self, app: FastAPI):
        self.app = app

    def stop(self):
        pass