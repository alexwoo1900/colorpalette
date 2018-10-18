import cv2
import numpy as np

from model import Colorbar


class Colorstrip(object):
    def __init__(self, conf):
        self._width = conf.colorstrip_width
        self._height = conf.colorstrip_height

        self.connected_to_bar = False

        self.b = None
        self._cm = None

    def connect(self, bar):
        if isinstance(bar, Colorbar):
            self.b = bar
            self.connected_to_bar = True
        else:
            raise Exception("Target object doesn't belong to Class 'Colorbar'")

    def correct_x(self, x):
        x = int(x)
        half_width = int(self._width / 2)
        _, x_max, _ = self._cm.shape
        if x < 0:
            return 0
        elif x + half_width >= x_max:
            return x_max - 1 - half_width
        else:
            return x

    def slide(self, x):
        self._cm = self.b.get_cm().copy()
        x = self.correct_x(x)

        half_width = int(self._width / 2)

        strip = np.array([[x - half_width,                0],
                          [x + half_width,                0],
                          [x + half_width, self._height - 1],
                          [x - half_width, self._height - 1]])

        # paint
        cv2.fillPoly(self._cm, np.int32([strip]), (0, 0, 255))
        # frame
        cv2.rectangle(self._cm, (x - half_width, 0), (x + half_width, self._height - 1), (0, 0, 0))

    def get_cm(self):
        return self._cm
