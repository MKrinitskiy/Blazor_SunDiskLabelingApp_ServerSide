from .BPaintVertex import *
from .PointD import *


class BPaintObject(object):
    def __init__(self, ObjectID: int,
                 VerticesList: dict,
                 Position: dict,
                 end: dict,
                 Scale: dict,
                 ObjectType: int):
        self.ObjectID = ObjectID
        self.VerticesList = list(map(BPaintVertex.from_json, VerticesList))
        self.Position = BPaintVertex.from_json(Position)
        self.end = BPaintVertex.from_json(end)
        self.Scale = PointD.from_json(Scale)
        self.ObjectType = ObjectType


    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)