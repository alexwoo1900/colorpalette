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
        x = (x, 0)[x < 0]
        x = (x, x_max - 1)[x >= x_max]

        strip = np.array([[x - self.width / 2, 0],
                          [x + self.width / 2, 0],
                          [x + self.width / 2, self.height - 1],
                          [x - self.width / 2, self.height - 1]])

        cv2.fillPoly(self.bar_matrix, np.int32([strip]), (255, 255, 255))

    def get_matrix(self):
        return self.bar_matrix
