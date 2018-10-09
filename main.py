import cv2

from model.Colorbar import Colorbar
from model.Colorboard import Colorboard
from model.Colorpin import Colorpin
from model.Colorstrip import Colorstrip
from utils.ColorConverter import ConvertType
from utils.ColorConverter import ColorConverter

if __name__ == '__main__':
    cv2.namedWindow('color_bar_demo')
    cv2.namedWindow('color_board_demo')

    colorbar = Colorbar(384, 20)
    bar_matrix = colorbar.get_matrix()

    colorboard = Colorboard(256, 256)
    colorboard.connect(colorbar)

    colorpin = Colorpin()
    colorpin.connect(colorboard)

    colorstrip = Colorstrip(4, 20)
    colorstrip.connect(colorbar)

    def on_mouse_action_in_colorbar(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN or (event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON):
            colorstrip.slide(x)
            bar_matrix = colorstrip.get_matrix()
            cv2.imshow('color_bar_demo', bar_matrix[:, :, ::-1])

            board_matrix = colorboard.get_submatrix_by_index(x)
            cv2.imshow('color_board_demo', board_matrix[:, :, ::-1])

    def on_mouse_action_in_colorboard(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN or (event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON):

            colorpin.locate(x, y)
            board_matrix = colorpin.get_matrix()
            cv2.imshow('color_board_demo', board_matrix[:, :, ::-1])

            rgb_color = colorboard.get_rgb_by_xy(x, y)
            r, g, b = rgb_color
            hex_color = ColorConverter.convert_rgb(rgb_color, ConvertType['RGB2HEX'])
            print('Hex:' + ('%#x' % hex_color))
            print('R:' + str(r) + ' G:' + str(g) + ' B:' + str(b))
            h, s, v = ColorConverter.convert_rgb(rgb_color, ConvertType['RGB2HSV'])
            print('H:' + str(h) + ' S:' + str(s) + ' V:' + str(v))
            h, s, l = ColorConverter.convert_rgb(rgb_color, ConvertType['RGB2HSL'])
            print('H:' + str(h) + ' S:' + str(s) + ' L:' + str(l))


    cv2.setMouseCallback('color_bar_demo', on_mouse_action_in_colorbar)
    cv2.setMouseCallback('color_board_demo', on_mouse_action_in_colorboard)

    # Need to convert RGB to BGR
    cv2.imshow('color_bar_demo', bar_matrix[:, :, ::-1])

    # Press 'Esc' to exit
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
