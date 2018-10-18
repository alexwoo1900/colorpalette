import math

from utils import ConvertType


class ColorConverter(object):
    def __init__(self):
        pass

    @staticmethod
    def convert(color, flag):
        if flag == ConvertType.RGB2HEX:
            r, g, b = color
            return (r << 16) + (g << 8) + b

        elif flag == ConvertType.RGB2HSV:
            r, g, b = [int(i) for i in color]
            h = -1
            m = max(r, g, b)
            n = min(r, g, b)

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

        elif flag == ConvertType.RGB2HSL:
            r, g, b = [int(i) for i in color]
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
            elif 0 < l <= 0.5:
                s = (m - n) / 255 / (2 * l)
            elif l > 0.5:
                s = (m - n) / 255 / (2 - 2 * l)

            l = l * 100
            s = s * 100

            return [round(h), round(s), round(l)]

        elif flag == ConvertType.HEX2RGB:
            return [(color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff]

        elif flag == ConvertType.HSV2RGB:
            h, s, v = color
            s, v = s / 100, v / 100

            h_x = math.floor(h / 60) % 6
            f = h / 60 - h_x
            p = round(255 * v * (1 - s))
            q = round(255 * v * (1 - f * s))
            t = round(255 * v * (1 - (1 - f) * s))
            v = round(255 * v)

            if h_x == 0:
                return [v, p, t]
            elif h_x == 1:
                return [q, v, p]
            elif h_x == 2:
                return [p, v, t]
            elif h_x == 3:
                return [p, q, v]
            elif h_x == 4:
                return [t, p, v]
            elif h_x == 5:
                return [v, p, q]

    @staticmethod
    def convert_op(color, flag):
        if flag == ConvertType.OPCV_RGB2HSV:
            r, g, b = [int(i) for i in color]
            h = -1
            m = max(r, g, b)
            n = min(r, g, b)

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
                s = (1 - n/m) * 255

            v = m

            return [round(h / 2), round(s), round(v)]

        elif flag == ConvertType.OPCV_HSV2RGB:
            h, s, v = color
            return ColorConverter.convert([h * 2, round(s * 100 / 255), round(v * 100 / 255)], ConvertType.HSV2RGB)
