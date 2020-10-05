class PointD(object):


    def __init__(self, X: float, Y: float):
        self.X = X
        self.Y = Y


    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)