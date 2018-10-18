import cv2

from model.Colorboard import Colorboard


class Colorpin(object):
    def __init__(self):
        self.connected_to_board = False

        self.b = None
        self._cm = None

        self.current_pos = (0, 0)

    def connect(self, board):
        if isinstance(board, Colorboard):
            self.b = board
            self.connected_to_board = True
        else:
            raise Exception("Target object doesn't belong to Class 'Colorboard'")

    def correct_xy(self, x, y):
        y_max, x_max, _ = self._cm.shape
        result_x, result_y = x, y
        if x < 0:
            result_x = 0
        elif x >= x_max:
            result_x = x_max - 1

        if y < 0:
            result_y = 0
        elif y >= y_max:
            result_y = y_max - 1
        return result_x, result_y

    def locate(self, x, y):
        if self.connected_to_board:
            self._cm = self.b.get_current_subcm().copy()
            self.current_pos = self.correct_xy(x, y)
            # paint
            cv2.circle(self._cm, self.current_pos, 2, (0, 0, 255), 1)
        else:
            raise Exception("Haven't connected to colorboard yet")

    def get_cm(self):
        return self._cm
