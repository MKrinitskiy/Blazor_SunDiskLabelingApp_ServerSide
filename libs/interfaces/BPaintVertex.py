from .PointD import *


class BPaintVertex(object):
    def __init__(self, PtD: dict):
        self.PtD = PointD.from_json(PtD)


    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)