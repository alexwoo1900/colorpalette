![colorpalette-logo](https://github.com/alexwoo1900/colorpalette/blob/master/docs/assets/colorpalette_logo.png)

Color palette written in Python and OpenCV

README: [ENGLISH](https://github.com/alexwoo1900/colorpalette/blob/master/README.md) | [简体中文](https://github.com/alexwoo1900/colorpalette/blob/master/README_CN.md)

## Demo

<div align=center><img src="https://github.com/alexwoo1900/colorpalette/blob/master/docs/assets/colorpalette.gif" alt="colorpalette-usage" /></div>

## How to use it

### Colorbar

#### Display Colorbar
```python
colorbar = Colorbar()                                                     # Create an instance of Colorbar
bar_matrix = colorbar.get_cm()                                            # Get matrix
cv2.imshow('color_bar_demo', cv2.cvtColor(bar_matrix, cv2.COLOR_HSV2BGR)) # Display colorbar
```
#### Colorstrip(slider)
```python
colorstrip = Colorstrip(conf)                                             # Create an instance of Colorstrip
colorstrip.connect(colorbar)                                              # Bind colorstrip to colorbar

colorstrip.slide(x)                                                       # Make the strip slide to x
bar_matrix = colorstrip.get_cm()                                          # Get matrix which contains colorbar and colorstrip
cv2.imshow('color_bar_demo', cv2.cvtColor(bar_matrix, cv2.COLOR_HSV2BGR)) # Display colorbar and colorstrip
```
#### Colorbar API

Colorbar.**get_cm()** \
Get computational matrix. Format: [row, column, color_in_hsv]

Colorbar.**get_color(x)** \
Get color by x value. Format: [h, s_max, v_max]

#### Colorstrip API

Colorstrip.**connect(bar)** \
Bind the strip to a colorbar

Colorstrip.**slide(x)** \
Make the strip slide to x

Colorstrip.**get_cm()** \
Get computational matrix. Format: [row, column, color_in_hsv]


### Colorboard

#### Display Colorboard
```python
colorboard = Colorboard(conf)                                                # Create an instance of Colorboard
colorboard.connect(colorbar)                                                 # Bind colorboard to colorbar

board_matrix = colorboard.get_subcm(x)                                       # Get matrix
cv2.imshow('color_board_demo', cv2.cvtColor(board_matrix, cv2.COLOR_HSV2BGR) # Display colorboard
```
#### Colorpin
```python
colorpin = Colorpin()                                                        # Create an instance of Colorpin
colorpin.connect(colorboard)                                                 # Bind colorpin to colorboard

colorpin.locate(x, y)                                                        # Put the pin to (x, y) in colorboard
board_matrix = colorpin.get_cm()                                             # Get matrix which contains colorboard and colorpin
cv2.imshow('color_board_demo', cv2.cvtColor(board_matrix, cv2.COLOR_HSV2BGR) # Display colorboard and colorpin
```
#### Colorboard API
Colorboard.**connect(bar)** \
Bind the board to a colorbar.

Colorboard.**get_current_subcm()** \
Get current sub computational matrix. Format: [row, column, color_in_hsv]

Colorboard.**get_subcm(hue)** \
Get sub computational matrix by a given hue. Format: [row, column, color_in_hsv]

Colorboard.**get_color(x, y)** \
Get color by (x, y). Format: [h, s, v]

Colorboard.**get_color_pos(color_in_hsv)** \
Get Color position by hsv. Format: [hue, row, column]

#### Colorpin API

Colorpin.**connect(board)** \
Bind the pin to a colorboard

Colorpin.**locate(x, y)** \
put the pin to (x, y) in colorboard

Colorpin.**get_cm()** \
Get computational matrix. Format: [row, column, color_in_hsv]

### Configuration

Section | Meaning
--- | ---
use_colorboard_rtcp | Real-time computing colorboard matrix
use_colorboard_cache | Use colorboard matrix cache

### TO-DO list
1. ~~Speed up the display of colorboard. (Optimize matrix calculation and compress cache file)~~
2. ~~Add Color-positioning~~
3. Add Colorpicker module

## License

MIT License
