import cv2

from model import Colorbar
from model import Colorboard
from model import Colorpin
from model import Colorstrip
from model import ColorConfiguration

from utils import ColorConverter
from utils import ConvertType

if __name__ == '__main__':
    config = ColorConfiguration()

    colorbar = Colorbar()

    colorboard = Colorboard(config)
    colorboard.connect(colorbar)

    colorpin = Colorpin()
    colorpin.connect(colorboard)

    colorstrip = Colorstrip()
    colorstrip.connect(colorbar)

    def on_mouse_action_in_colorbar(event, x, y, flags, param):
        if (event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON) or event == cv2.EVENT_LBUTTONDOWN:
            colorstrip.slide(x)
            colorstrip_cm = colorstrip.get_cm()
            cv2.imshow('color_bar_demo', cv2.cvtColor(colorstrip_cm, cv2.COLOR_HSV2BGR))

            colorboard_cm = colorboard.get_subcm(x)
            cv2.imshow('color_board_demo', cv2.cvtColor(colorboard_cm, cv2.COLOR_HSV2BGR))

    def on_mouse_action_in_colorboard(event, x, y, flags, param):
        if (event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON) or event == cv2.EVENT_LBUTTONDOWN:
            colorpin.locate(x, y)
            colorpin_cm = colorpin.get_cm()
            cv2.imshow('color_board_demo', cv2.cvtColor(colorpin_cm, cv2.COLOR_HSV2BGR))
            hsv = colorboard.get_color(x, y)
            r, g, b = ColorConverter.convert_op(hsv, ConvertType.OPCV_HSV2RGB)
            print('R:' + str(r) + ' G:' + str(g) + ' B:' + str(b))

    cv2.namedWindow('color_bar_demo')
    cv2.namedWindow('color_board_demo')

    cv2.setMouseCallback('color_bar_demo', on_mouse_action_in_colorbar)
    cv2.setMouseCallback('color_board_demo', on_mouse_action_in_colorboard)

    colorbar_dm = colorbar.get_cm()

    colorstrip.slide(0)
    colorstrip_cm = colorstrip.get_cm()
    cv2.imshow('color_bar_demo', cv2.cvtColor(colorstrip_cm, cv2.COLOR_HSV2BGR))

    colorboard_cm = colorboard.get_subcm(0)
    cv2.imshow('color_board_demo', cv2.cvtColor(colorboard_cm, cv2.COLOR_HSV2BGR))

    colorpin.locate(0, 0)
    colorpin_cm = colorpin.get_cm()
    cv2.imshow('color_board_demo', cv2.cvtColor(colorpin_cm, cv2.COLOR_HSV2BGR))

    cv2.waitKey(1)
    
    r, g, b = map(int, input('Input your RGB\n').split())
    hsv = ColorConverter.convert_op([r, g, b], ConvertType.OPCV_RGB2HSV)

    bar_x, board_y, board_x = colorboard.get_color_pos(hsv)
    colorstrip.slide(bar_x)
    colorstrip_cm = colorstrip.get_cm()
    cv2.imshow('color_bar_demo', cv2.cvtColor(colorstrip_cm, cv2.COLOR_HSV2BGR))

    colorboard_cm = colorboard.get_subcm(bar_x)
    cv2.imshow('color_board_demo', cv2.cvtColor(colorboard_cm, cv2.COLOR_HSV2BGR))

    colorpin.locate(board_x, board_y)
    colorpin_cm = colorpin.get_cm()
    cv2.imshow('color_board_demo', cv2.cvtColor(colorpin_cm, cv2.COLOR_HSV2BGR))

    hsv = colorboard.get_color(board_x, board_y)
    r, g, b = ColorConverter.convert_op(hsv, ConvertType.OPCV_HSV2RGB)
    print('R:' + str(r) + ' G:' + str(g) + ' B:' + str(b))

    while True:
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
