import os
import logging
import configparser

import datetime

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
        start_r, start_g, start_b = 255, 255, 255
        end_r, end_g, end_b = color
        start_col_interval = -255 / self.width
        end_col_r_interval = end_r * -1 / self.width
        end_col_g_interval = end_g * -1 / self.width
        end_col_b_interval = end_b * -1 / self.width

        r_interval = (end_r - start_r) / self.width
        g_interval = (end_g - start_g) / self.width
        b_interval = (end_b - start_b) / self.width
        # starttime = datetime.datetime.now()
        for row in range(self.height):
            if r_interval != 0:
                row_r = np.arange(start_r, end_r+1e-6, r_interval).reshape(self.width, 1)
            else:
                row_r = np.full((self.width,), end_r).reshape(self.width, 1)
            if g_interval != 0:
                row_g = np.arange(start_g, end_g+1e-6, g_interval).reshape(self.width, 1)
            else:
                row_g = np.full((self.width,), end_g).reshape(self.width, 1)
            if b_interval != 0:
                row_b = np.arange(start_b, end_b+1e-6, b_interval).reshape(self.width, 1)
            else:
                row_b = np.full((self.width,), end_b).reshape(self.width, 1)

            row_rgb = np.hstack((row_r, row_g, row_b))
            self.colorboard_matrix[index, row, ] = row_rgb

            start_r, start_g, start_b = start_r + start_col_interval, start_g + start_col_interval, start_b + start_col_interval
            end_r, end_g, end_b = end_r + end_col_r_interval, end_g + end_col_g_interval, end_b + end_col_b_interval
            r_interval = (end_r - start_r) / self.width
            g_interval = (end_g - start_g) / self.width
            b_interval = (end_b - start_b) / self.width
        # endtime = datetime.datetime.now()
        # print((endtime-starttime).microseconds)


    def generate_colorboard_matrix(self, caching_flag):
        for index in range(self.matrix_count):
            color = self.bar.get_rgb_by_x(index)
            start_r, start_g, start_b = 255, 255, 255
            end_r, end_g, end_b = color
            start_col_interval = -255 / self.width
            end_col_r_interval = end_r * -1 / self.width
            end_col_g_interval = end_g * -1 / self.width
            end_col_b_interval = end_b * -1 / self.width

            r_interval = (end_r - start_r) / self.width
            g_interval = (end_g - start_g) / self.width
            b_interval = (end_b - start_b) / self.width
            for row in range(self.height):
                if r_interval != 0:
                    row_r = np.arange(start_r, end_r+1e-6, r_interval).reshape(self.width, 1)
                else:
                    row_r = np.full((self.width,), end_r).reshape(self.width, 1)
                if g_interval != 0:
                    row_g = np.arange(start_g, end_g+1e-6, g_interval).reshape(self.width, 1)
                else:
                    row_g = np.full((self.width,), end_g).reshape(self.width, 1)
                if b_interval != 0:
                    row_b = np.arange(start_b, end_b+1e-6, b_interval).reshape(self.width, 1)
                else:
                    row_b = np.full((self.width,), end_b).reshape(self.width, 1)

                row_rgb = np.hstack((row_r, row_g, row_b))
                self.colorboard_matrix[index, row, ] = row_rgb

                start_r, start_g, start_b = start_r + start_col_interval, start_g + start_col_interval, start_b + start_col_interval
                end_r, end_g, end_b = end_r + end_col_r_interval, end_g + end_col_g_interval, end_b + end_col_b_interval
                r_interval = (end_r - start_r) / self.width
                g_interval = (end_g - start_g) / self.width
                b_interval = (end_b - start_b) / self.width

        if caching_flag:
            try:
                self.colorboard_matrix.tofile('cache/colorboard.mtx')
            except Exception as err:
                raise err

    def get_current_submatrix(self):
        return self.get_submatrix_by_index(self.current_matrix_index)

    def correct_index(self, index):
        index = (index, 0)[index < 0]
        index = (index, self.matrix_count - 1)[index >= self.matrix_count]
        return index

    def correct_position(self, x, y):
        _, y_max, x_max, _ = self.colorboard_matrix.shape
        x = (x, 0)[x < 0]
        x = (x, x_max-1)[x >= x_max]
        y = (y, 0)[y < 0]
        y = (y, y_max-1)[y >= y_max]
        return x, y

    def get_submatrix_by_index(self, index):
        if self.connected:
            self.current_matrix_index = self.correct_index(index)
            if self.rtcp_on:
                self.generate_colorboard_submatrix(self.current_matrix_index)
            return self.colorboard_matrix[self.current_matrix_index, ]
        else:
            raise Exception("Haven't connected to colorbar yet")

    def get_rgb_by_xy(self, x, y):
        if self.connected:
            x, y = self.correct_position(x, y)
            return self.colorboard_matrix[self.current_matrix_index, y, x, ]
        else:
            raise Exception("Haven't connected to colorbar yet")
