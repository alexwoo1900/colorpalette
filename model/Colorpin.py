import cv2

from model.Colorboard import Colorboard


class Colorpin(object):
    def __init__(self):
        self.board = None
        self.pinboard_matrix = None
        self.connected = False
        self.current_locate = (0, 0)

    def connect(self, board):
        if isinstance(board, Colorboard):
            self.board = board
            self.connected = True
        else:
            raise Exception("Target object doesn't belong to Class 'Colorboard'")

    def correct_position(self, x, y):
        y_max, x_max, _ = self.pinboard_matrix.shape
        x = (x, 0)[x < 0]
        x = (x, x_max-1)[x >= x_max]
        y = (y, 0)[y < 0]
        y = (y, y_max-1)[y >= y_max]
        return x, y

    def locate(self, x, y):
        if self.connected:
            self.pinboard_matrix = self.board.get_current_submatrix().copy()
            self.current_locate = self.correct_position(x, y)
            # paint
            cv2.circle(self.pinboard_matrix, self.current_locate, 2, (255, 255, 255), 1)
        else:
            raise Exception("Haven't connected to colorboard yet")

    def get_matrix(self):
        return self.pinboard_matrix
