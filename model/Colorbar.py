import numpy as np


class Colorbar(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.colorbar_matrix = np.zeros((self.height, self.width, 3), np.uint8)

        self.initialize_matrix()

    '''
    If you want to change the initial display of colorbar, rewrite this function
    '''
    def initialize_matrix(self):

        interval = int(self.width / 6)
        scale = 256 / interval

        # Color Segment 1
        for i in range(interval):
            self.colorbar_matrix[:, i, ] = [255, 0, i*scale]

        # Color Segment 2
        for i in range(interval):
            self.colorbar_matrix[:, interval+i, ] = [255-i*scale, 0, 255]

        # Color Segment 3
        for i in range(interval):
            self.colorbar_matrix[:, interval*2+i, ] = [0, i*scale, 255]

        # Color Segment 4
        for i in range(interval):
            self.colorbar_matrix[:, interval*3+i, ] = [0, 255, 255-i*scale]

        # Color Segment 5
        for i in range(interval):
            self.colorbar_matrix[:, interval*4+i, ] = [i*scale, 255, 0]

        # Color Segment 6
        for i in range(interval):
            self.colorbar_matrix[:, interval*5+i, ] = [255, 255-i*scale, 0]

    def correct_position(self, x):
        _, x_max, _ = self.colorbar_matrix.shape
        x = (x, x_max-1)[x >= x_max]
        x = (x, 0)[x < 0]
        return x

    def get_matrix(self):
        return self.colorbar_matrix

    def get_rgb_by_x(self, x):
        x = self.correct_position(x)
        return self.colorbar_matrix[0, x, ]
