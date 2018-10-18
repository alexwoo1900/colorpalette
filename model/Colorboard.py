import os
import logging

import numpy as np

from model import Global
from .Colorbar import Colorbar


class Colorboard(object):
    def __init__(self, conf):
        self.conf = conf

        self.b = None
        self.connected_to_bar = False
        self.current_hue = -1

        # Computational Matrix
        self._cm = np.zeros((Global.OPCV_HUE_SIZE,
                             Global.OPCV_VAL_SIZE,
                             Global.OPCV_SAT_SIZE,
                             Global.HSV_COMPONENT_SIZE), dtype=np.uint8)

    def connect(self, bar):
        if isinstance(bar, Colorbar):
            self.b = bar
            self.connected_to_bar = True
            try:
                self.prepare()
            except Exception as err:
                raise err
        else:
            raise Exception("Target object doesn't belong to Class 'Colorbar'")

    def prepare(self):
        if self.conf.colorboard_cache_on:
            if os.path.exists('cache/colorboard.mtx') and os.path.isfile('cache/colorboard.mtx'):
                try:
                    self.load_cached_cm()
                except Exception as err:
                    raise err
            else:
                logging.debug('No colorboard cache, generating new one...')
                try:
                    self.generate_cm(True)
                except Exception as err:
                    raise err
        elif not self.conf.colorboard_cache_on and not self.conf.colorboard_rtcp_on:
            self.generate_cm(False)

    def load_cached_cm(self):
        try:
            data = np.fromfile('cache/colorboard.mtx', np.uint8)
            data.shape = Global.OPCV_HUE_SIZE, Global.OPCV_VAL_SIZE, Global.OPCV_SAT_SIZE, Global.HSV_COMPONENT_SIZE
            self._cm = data
        except Exception as err:
            raise err

    def generate_cm(self, caching):
        for i in range(Global.OPCV_HUE_SIZE):
            self.generate_subcm(i)

        if caching:
            try:
                self._cm.tofile('cache/colorboard.mtx')
            except Exception as err:
                raise err

    @staticmethod
    def correct_hue(h):
        if h < 0:
            return 0
        elif h > Global.OPCV_HUE_MAX:
            return Global.OPCV_HUE_MAX
        else:
            return h

    def generate_subcm(self, hue):
        # Saturation array
        s_arr = np.arange(Global.OPCV_SAT_MIN, Global.OPCV_SAT_MAX + 1e-6, 1)
        # Saturation matrix
        s_m = np.tile(s_arr, Global.OPCV_VAL_SIZE).reshape(Global.OPCV_VAL_SIZE, Global.OPCV_SAT_SIZE, 1)
        # Value array
        v_arr = np.arange(Global.OPCV_VAL_MAX, Global.OPCV_VAL_MIN - 1e-6, -1)
        # Value matrix
        v_m = np.transpose(np.tile(v_arr, Global.OPCV_SAT_SIZE).reshape(Global.OPCV_SAT_SIZE, Global.OPCV_VAL_SIZE)).reshape(Global.OPCV_VAL_SIZE, Global.OPCV_SAT_SIZE, 1)
        # Hue matrix
        h_m = np.full((Global.OPCV_VAL_SIZE, Global.OPCV_SAT_SIZE, 1), hue)
        # Sub Computational Matrix
        hsv_m = np.dstack((h_m, s_m, v_m)).reshape(Global.OPCV_VAL_SIZE, Global.OPCV_SAT_SIZE, Global.HSV_COMPONENT_SIZE)

        self._cm[hue, ] = hsv_m

    def get_subcm(self, hue):
        if self.connected_to_bar:
            self.current_hue = Colorboard.correct_hue(hue)
            if self.conf.colorboard_rtcp_on:
                self.generate_subcm(self.current_hue)
            return self._cm[self.current_hue, ]
        else:
            raise Exception("Haven't connected to colorbar yet")

    def get_current_subcm(self):
        return self.get_subcm(self.current_hue)

    def correct_xy(self, x, y):
        _, y_max, x_max, _ = self._cm.shape
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

    def get_color(self, x, y):
        if self.connected_to_bar:
            x, y = self.correct_xy(x, y)
            return self._cm[self.current_hue, y, x, ]
        else:
            raise Exception("Haven't connected to colorbar yet")

    def get_color_pos(self, color):
        h, s, v = color
        return h, 255 - v, s
