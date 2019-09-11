import numpy as np


class Point(object):
    def __init__(self, x, y):
        self.X = np.int32(x)
        self.Y = np.int32(y)

class PointF(object):
    def __init__(self, x, y):
        self.X = np.float32(x)
        self.Y = np.float32(y)

class PointD(object):
    def __init__(self, x, y):
        self.X = np.float64(x)
        self.Y = np.float64(y)

class Size(object):
    def __init__(self, w, h):
        self.Width = np.int32(w)
        self.Height = np.int32(h)


class SizeF(object):
    def __init__(self, w, h):
        self.Width = np.float32(w)
        self.Height = np.float32(h)


class SizeD(object):
    def __init__(self, w, h):
        self.Width = np.float64(w)
        self.Height = np.float64(h)