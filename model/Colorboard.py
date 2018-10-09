import os
import logging
import configparser

import numpy as np

from .Colorbar import Colorbar


class Colorboard(object):
    def __init__(self, width, height):
        self.config = None
        self.bar = None
        self.colorboard_matrix = None
        self.matrix_count = -1
        self.connected = False
        self.current_matrix_index = 0
        self.rtcp_on = False

        self.width = width
        self.height = height

    def connect(self, bar):
        if isinstance(bar, Colorbar):
            self.bar = bar
            self.matrix_count = self.bar.width
            self.colorboard_matrix = np.zeros((self.matrix_count, self.height, self.width, 3), np.uint8)
            self.connected = True
            try:
                self.load_config()
            except Exception as err:
                raise err
        else:
            raise Exception("Target object doesn't belong to Class 'Colorbar'")

    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        if int(self.config['color']['use_colorboard_cache']):
            if os.path.exists('cache/colorboard.mtx') and os.path.isfile('cache/colorboard.mtx'):
                try:
                    self.load_cached_colorboard_matrix()
                except Exception as err:
                    raise err
            else:
                logging.debug('No colorboard cache, generating new one...')
                try:
                    self.generate_colorboard_matrix(True)
                except Exception as err:
                    raise err
        elif int(self.config['color']['use_colorboard_rtcp']):
            self.rtcp_on = True
        else:
            self.generate_colorboard_matrix(False)

    def load_cached_colorboard_matrix(self):
        try:
            data = np.fromfile('cache/colorboard.mtx', np.uint8)
            data.shape = self.matrix_count, self.height, self.width, 3
            self.colorboard_matrix = data
        except Exception as err:
            raise err

    def generate_colorboard_submatrix(self, index):
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
            try:
                self.colorboard_matrix.tofile('cache/colorboard.mtx')
            except Exception as err:
                raise err

    def get_current_matrix(self):
        self.get_submatrix_by_index(self.current_matrix_index)

    def get_submatrix_by_index(self, index):
        if self.connected:
            self.current_matrix_index = index
            if self.rtcp_on:
                self.generate_colorboard_submatrix(self.current_matrix_index)
            return self.colorboard_matrix[self.current_matrix_index, ]
        else:
            raise Exception("Haven't connected to colorbar yet")

    def get_rgb_by_xy(self, x, y):
        if self.connected:
            _, y_max, x_max, _ = self.colorboard_matrix.shape
            x = (x, 0)[x < 0]
            x = (x, x_max-1)[x >= x_max]
            y = (y, 0)[y < 0]
            y = (y, y_max-1)[y >= y_max]
            return self.colorboard_matrix[self.current_matrix_index, y, x, ]
        else:
            raise Exception("Haven't connected to colorbar yet")
