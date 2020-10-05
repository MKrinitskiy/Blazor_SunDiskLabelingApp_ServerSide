class SizeD(object):


    def __init__(self, Width: float, Height: float):
        self.Width = Width
        self.Height = Height


    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)