import os
import cv2
import logging
import configparser
import numpy as np


def rgb2hex(color_in_rgb):
    r, g, b = color_in_rgb
    return (r << 16) + (g << 8) + b


def hex2rgb(color_in_hex):
    return [(color_in_hex >> 16) & 0xff, (color_in_hex >> 8) & 0xff, color_in_hex & 0xff]

def rgb2hsv(color_in_rgb):
    r, g, b = [int(i) for i in color_in_rgb]
    m = max(r, g, b)
    n = min(r, g, b)

    h = -1

    if m == n:
        h = 0
    elif m == r and g >= b:
        h = 60 * (g - b) / (m - n)
    elif m == r and g < b:
        h = 60 * (g - b) / (m - n) + 360
    elif m == g:
        h = 60 * (b - r) / (m - n) + 120
    elif m == b:
        h = 60 * (r - g) / (m - n) + 240

    if m == 0:
        s = 0
    else:
        s = (1 - n/m) * 100

    v = m * 100 / 255

    return [round(h), round(s), round(v)]


def rgb2hsl(color_in_rgb):
    r, g, b = [int(i) for i in color_in_rgb]
    m = max(r, g, b)
    n = min(r, g, b)

    h = s = -1

    if m == n:
        h = 0
    elif m == r and g >= b:
        h = 60 * (g - b) / (m - n)
    elif m == r and g < b:
        h = 60 * (g - b) / (m - n) + 360
    elif m == g:
        h = 60 * (b - r) / (m - n) + 120
    elif m == b:
        h = 60 * (r - g) / (m - n) + 240

    l = (m + n) / 2 / 255

    if l == 0 or m == n:
        s = 0
    elif 0 < l and l <= 0.5:
        s = (m - n) / 255 / (2 * l)
    elif l > 0.5:
        s = (m - n) / 255 / (2 - 2 * l)

    l = l * 100
    s = s * 100

    return [round(h), round(s), round(l)]


class Colorbar(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.colorbar_matrix = np.zeros((self.height, self.width, 3), np.uint8)

        self.initialize_matrix()

    def initialize_matrix(self):

        interval = int(self.width / 6)
        scale = 256 / interval

        # segment1
        for i in range(interval):
            self.colorbar_matrix[:, i, ] = [255, 0, i*scale]

        # segment2
        for i in range(interval):
            self.colorbar_matrix[:, interval+i, ] = [255-i*scale, 0, 255]

        # segment3
        for i in range(interval):
            self.colorbar_matrix[:, interval*2+i, ] = [0, i*scale, 255]

        # segment4
        for i in range(interval):
            self.colorbar_matrix[:, interval*3+i, ] = [0, 255, 255-i*scale]

        # segment5
        for i in range(interval):
            self.colorbar_matrix[:, interval*4+i, ] = [i*scale, 255, 0]

        # segment6
        for i in range(interval):
            self.colorbar_matrix[:, interval*5+i, ] = [255, 255-i*scale, 0]

    def get_ui_matrix(self):
        return self.colorbar_matrix

    def get_rgb_by_x(self, x):
        return self.colorbar_matrix[0, x, ]


class Colorboard(object):
    def __init__(self, width, height, bar):
        self.config = None
        self.width = width
        self.height = height
        self.bar = bar
        self.current_matrix_index = -1
        self.matrix_count = bar.width
        self.colorboard_matrix = np.zeros((self.matrix_count, self.height, self.width, 3), np.uint8)

        self.load_config()

    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        if self.config['color']['use_colorboard_cache']:
            if os.path.exists('cache/colorboard.mtx') and os.path.isfile('cache/colorboard.mtx'):
                try:
                    self.load_cached_colorboard_matrix()
                except Exception as err:
                    raise err
            else:
                logging.warning('No colorboard cache!')
                self.generate_colorboard_matrix(True)
        else:
            self.generate_colorboard_matrix(False)

    def load_cached_colorboard_matrix(self):
        try:
            data = np.fromfile('cache/colorboard.mtx', np.uint8)
            data.shape = self.matrix_count, self.height, self.width, 3
            self.colorboard_matrix = data
        except Exception as err:
            raise err

    def generate_colorboard_matrix(self, caching_flag):
        for index in range(self.matrix_count):
            color = self.bar.get_rgb_by_x(index)
            target_color = np.array(color)
            end_col_interval = -1 * target_color / self.height

            start_col_interval = np.array([-1 * 0x100 / self.height,
                                           -1 * 0x100 / self.height,
                                           -1 * 0x100 / self.height])

            start_color = np.array([0xff, 0xff, 0xff])
            end_color = target_color
            row_interval = (end_color - start_color) / self.width

            for row in range(self.height):
                current_color = start_color
                for height in range(self.width):
                    self.colorboard_matrix[index, row, height, ] = current_color
                    current_color = current_color + row_interval
                start_color = start_color + start_col_interval
                end_color = end_color + end_col_interval

                row_interval = (end_color - start_color) / self.width

        if caching_flag:
            self.colorboard_matrix.tofile('cache/colorboard.mtx')

    def get_current_matrix(self):
        return self.colorboard_matrix[self.current_matrix_index, ]

    def get_ui_matrix(self, index):
        self.current_matrix_index = index
        return self.colorboard_matrix[self.current_matrix_index, ]

    def get_rgb_by_xy(self, x, y):
        return self.colorboard_matrix[self.current_matrix_index, y, x, ]

class Colorpin(object):
    def __init__(self):
        self.board = None
        self.pinboard_matrix = None

    def connect(self, board):
        self.board = board

    def locate(self, x, y):
        self.pinboard_matrix = self.board.get_current_matrix().copy()
        cv2.circle(self.pinboard_matrix, (x, y), 2, (0, 0, 0), 1)

    def get_ui_matrix(self):
        return self.pinboard_matrix

if __name__ == '__main__':
    cv2.namedWindow('color_bar_demo')
    cv2.namedWindow('color_board_demo')

    colorbar = Colorbar(384, 20)
    bar_matrix = colorbar.get_ui_matrix()

    colorboard = Colorboard(256, 256, colorbar)

    colorpin = Colorpin()
    colorpin.connect(colorboard)


    def on_mouse_action_in_colorbar(event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            board_matrix = colorboard.get_ui_matrix(x)
            cv2.imshow('color_board_demo', board_matrix[:, :, ::-1])

    def on_mouse_action_in_colorboard(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            colorpin.locate(x, y)
            board_matrix = colorpin.get_ui_matrix()
            cv2.imshow('color_board_demo', board_matrix[:, :, ::-1])

            rgb_color = colorboard.get_rgb_by_xy(x, y)
            r, g, b = rgb_color
            hex_color = rgb2hex(rgb_color)
            hsv_color = rgb2hsv(rgb_color)
            h, s, v = hsv_color
            print('R:' + str(r) + ' G:' + str(g) + ' B:' + str(b) + '\n')
            print('Hex:' + ('%#x' % hex_color) + '\n')
            print('H:' + str(h) + ' S:' + str(s) + ' V:' + str(v) + '\n')
            h, s, l = rgb2hsl(rgb_color)
            print('H:' + str(h) + ' S:' + str(s) + ' L:' + str(l) + '\n')



    cv2.setMouseCallback('color_bar_demo', on_mouse_action_in_colorbar)
    cv2.setMouseCallback('color_board_demo', on_mouse_action_in_colorboard)

    while True:
        cv2.imshow('color_bar_demo', bar_matrix[:, :, ::-1])
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
