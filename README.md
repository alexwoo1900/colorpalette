![colorpalette-logo](https://github.com/alexwoo1900/colorpalette/blob/master/docs/assets/colorpalette_logo.png)

Color palette written in Python and OpenCV

README: [ENGLISH](https://github.com/alexwoo1900/colorpalette/blob/master/README.md) | [简体中文](https://github.com/alexwoo1900/colorpalette/blob/master/README_CN.md)

## Demo

<div align=center><img src="https://github.com/alexwoo1900/colorpalette/blob/master/docs/assets/colorpalette.gif" alt="colorpalette-usage" /></div>

## How to use it

### Colorbar

#### Display Colorbar
```python
colorbar = Colorbar(384, 20)                            # Create an instance of Colorbar
bar_matrix = colorbar.get_matrix()                      # Get color matrix
cv2.imshow('color_bar_demo', bar_matrix[:, :, ::-1])    # Display colorbar
```
#### Colorstrip(slider)
```python
colorstrip = Colorstrip(4, 20)                          # Create an instance of Colorstrip
colorstrip.connect(colorbar)                            # Bind colorstrip to colorbar

colorstrip.slide(x)                                     # Make the strip slide to x
bar_matrix = colorstrip.get_matrix()                    # Get color matrix which contains colorbar and colorstrip
cv2.imshow('color_bar_demo', bar_matrix[:, :, ::-1])    # Display colorbar and colorstrip
```
#### Colorbar API

Colorbar.**get_matrix()** \
Get color matrix. Format: [row, column, color]

Colorbar.**get_rgb_by_x(x)** \
Get color in RGB by x value. Format: [r, g, b]

#### Colorstrip API

Colorstrip.**connect(bar)** \
Bind the strip to a colorbar

Colorstrip.**slide(x)** \
Make the strip slide to x

Colorstrip.**get_matrix()** \
Get color matrix. Format: [row, column, color]


### Colorboard

#### Display Colorboard
```python
colorboard = Colorboard(256, 256)                       # Create an instance of Colorboard
colorboard.connect(colorbar)                            # Bind colorboard to colorbar

board_matrix = colorboard.get_submatrix_by_index(x)     # Get color matrix
cv2.imshow('color_board_demo', board_matrix[:, :, ::-1])# Display colorboard
```
#### Colorpin
```python
colorpin = Colorpin()                                   # Create an instance of Colorpin
colorpin.connect(colorboard)                            # Bind colorpin to colorboard

colorpin.locate(x, y)                                   # Put the pin to (x, y) in colorboard
board_matrix = colorpin.get_matrix()                    # Get color matrix which contains colorboard and colorpin
cv2.imshow('color_board_demo', board_matrix[:, :, ::-1])# Display colorboard and colorpin
```
#### Colorboard API
Colorboard.**connect(bar)** \
Bind the board to a colorbar. The colorboard creates the matrix based on color gamut of target colorbar

Colorboard.**get_current_submatrix()** \
Get current submatrix. Format: [row, column, color]

Colorboard.**get_submatrix_by_index(index)** \
Get submatrix by a given index, like get_current_submatrix

Colorboard.**get_rgb_by_xy(x, y)** \
Get color in RGB by (x, y). Format: [r, g, b]

#### Colorpin API

Colorpin.**connect(board)** \
Bind the pin to a colorboard

Colorpin.**locate(x, y)** \
put the pin to (x, y) in colorboard

Colorpin.**get_matrix()** \
Get color matrix. Format: [row, column, color]

### Configuration

Section | Meaning
--- | ---
use_colorboard_rtcp | Real-time computing colorboard matrix
use_colorboard_cache | Use colorboard matrix cache

### To-do list
1. Speed up the display of colorboard. (Optimize matrix calculation and compress cache file) 
2. Add Color-positioning
3. Add Colorpicker module

