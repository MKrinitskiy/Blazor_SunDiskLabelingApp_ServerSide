from .BPaintObject import *
from .SizeD import *

class ExampleLabels(object):
    def __init__(self, LabelsList: list,
                 strBaseImageFilename: str,
                 PresentedImageSize: dict):
        self.LabelsList = list(map(BPaintObject.from_json, LabelsList))
        self.strBaseImageFilename = strBaseImageFilename
        self.PresentedImageSize = SizeD.from_json(PresentedImageSize)


    @classmethod
    def from_json(cls, data: dict):
        return cls(**data)