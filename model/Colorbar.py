import numpy as np

from model import Global

class Colorbar(object):
    def __init__(self):
        # Computational Matrix, base on HSV
        self._cm = np.zeros((10, Global.OPCV_HUE_SIZE, Global.HSV_COMPONENT_SIZE), dtype=np.uint8)

        self.init_cm()

    def init_cm(self):
        for i in range(Global.OPCV_HUE_SIZE):
            self._cm[:, i, ] = [i, Global.OPCV_SAT_MAX, Global.OPCV_VAL_MAX]

    def correct_x(self, x):
        _, x_max, _ = self._cm.shape
        if x >= x_max:
            return x_max - 1
        elif x < 0:
            return 0
        else:
            return x

    def get_color(self, x):
        x = self.correct_x(x)
        return self._cm[0, x, ]

    def get_cm(self):
        return self._cm
