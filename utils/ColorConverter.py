from enum import IntEnum


class ConvertType(IntEnum):
    RGB2HEX = 1
    RGB2HSV = 2
    RGB2HSL = 3


class ColorConverter(object):
    def __init__(self):
        pass

    @staticmethod
    def convert_rgb(color, flag):
        if flag == ConvertType['RGB2HEX']:
            r, g, b = color
            return (r << 16) + (g << 8) + b

        elif flag == ConvertType['RGB2HSV']:
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

        elif flag == ConvertType['RGB2HSL']:
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
            elif 0 < l and l <= 0.5:
                s = (m - n) / 255 / (2 * l)
            elif l > 0.5:
                s = (m - n) / 255 / (2 - 2 * l)

            l = l * 100
            s = s * 100

            return [round(h), round(s), round(l)]

    @staticmethod
    def convert_hex(color, flag):
        if flag == ConvertType['HEX2RGB']:
            return [(color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff]
