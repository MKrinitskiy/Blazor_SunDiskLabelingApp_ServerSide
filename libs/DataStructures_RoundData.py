from .DataStructures_Geometry import *
import numpy as np



class RoundDataWithUnderlyingImgSize(object):
    def __init__(self, circleRoundData, imgSize):
        if type(circleRoundData) is not RoundData:
            raise TypeError("circleRoundData parameter should be of type RoundData")
        if type(imgSize) is not Size:
            raise TypeError("imgSize parameter should be of type SizeD")
        self.circle = circleRoundData
        self.imgSize = imgSize



class RoundData(object):
    def __init__(self, centerX, centerY, radius):
        self.IntCenterX = np.int32(centerX)
        self.IntCenterY = np.int32(centerY)
        self.DCenterX = np.float64(centerX)
        self.DCenterY = np.float64(centerY)
        self.DRadius = radius
        self.IsNull = False