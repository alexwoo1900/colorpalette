import cv2
import numpy as np


class Colorstrip(object):
    def __init__(self, width, height):
        self.bar = None
        self.bar_matrix = None

        self.width = width
        self.height = height

    def connect(self, bar):
        self.bar = bar

    def slide(self, x):
        self.bar_matrix = self.bar.get_matrix().copy()
        _, x_max, _ = self.bar_matrix.shape

        half_width = int(self.width / 2)
        x = (x, 0)[x < 0]
        x = (x, x_max - 1 - half_width)[x + half_width >= x_max]

        strip = np.array([[x - half_width, 0],
                          [x + half_width, 0],
                          [x + half_width, self.height - 1],
                          [x - half_width, self.height - 1]])

        cv2.fillPoly(self.bar_matrix, np.int32([strip]), (222, 222, 222))

        # frame
        cv2.rectangle(self.bar_matrix, (x - half_width, 0), (x + half_width, self.height - 1), (161, 161, 161))

    def get_matrix(self):
        return self.bar_matrix
