import numpy as np


class Box:

    def __init__(self, xy, x1y1):
        self.x = xy[0]
        self.y = xy[1]
        self.x1 = x1y1[0]
        self.y1 = x1y1[1]
        self.org = None
        self.clicked = False

    def set_original(self, img: np.ndarray):
        self.org = img.copy()


if __name__ == '__main__':
    pass
