![colorpalette-logo](https://github.com/alexwoo1900/colorpalette/blob/master/docs/assets/colorpalette_logo.png)

用Python和penCV编写的调色板工具

README: [ENGLISH](https://github.com/alexwoo1900/colorpalette/blob/master/README.md) | [简体中文](https://github.com/alexwoo1900/colorpalette/blob/master/README_CN.md)

## Demo演示

<div align=center><img src="https://github.com/alexwoo1900/colorpalette/blob/master/docs/assets/colorpalette.gif" alt="colorpalette-usage" /></div>

## 如何使用该工程

### 颜色条

#### 显示颜色条
```python
colorbar = Colorbar()                                                     # 创建颜色条对象
bar_matrix = colorbar.get_cm()                                            # 获取颜色条计算矩阵
cv2.imshow('color_bar_demo', cv2.cvtColor(bar_matrix, cv2.COLOR_HSV2BGR)) # 将计算矩阵放到窗口上显示
```
#### 颜色滑动块
```python
colorstrip = Colorstrip(conf)                                             # 创建滑动块对象
colorstrip.connect(colorbar)                                              # 将滑动块绑定到颜色条上

colorstrip.slide(x)                                                       # 让滑动块滑动到x位置处
bar_matrix = colorstrip.get_cm()                                          # 获取已绘制滑动块的颜色条计算矩阵
cv2.imshow('color_bar_demo', cv2.cvtColor(bar_matrix, cv2.COLOR_HSV2BGR)) # 将计算矩阵放到窗口上显示
```
#### 颜色条API

Colorbar.**get_cm()** \
获取颜色条计算矩阵，格式为[row, column, color_in_hsv]

Colorbar.**get_color(x)** \
根据x值来获取OpenCV坐标x轴上对应位置的HSV颜色值，格式为[h, s_max, v_max]

#### 滑动块API

Colorstrip.**connect(bar)** \
绑定已存在的Colorbar对象

Colorstrip.**slide(x)** \
滑动并绘制滑动块到x处

Colorstrip.**get_cm()** \
获取绘制滑动块后颜色条的计算矩阵,返回值的格式为[row, column, color_in_hsv]


### 取色版

#### 显示取色版
```python
colorboard = Colorboard(conf)                                                # 创建取色版对象
colorboard.connect(colorbar)                                                 # 将取色版绑定到颜色条上

board_matrix = colorboard.get_subcm(x)                                       # 获取取色版的计算矩阵
cv2.imshow('color_board_demo', cv2.cvtColor(board_matrix, cv2.COLOR_HSV2BGR) # 将计算矩阵放到窗口上显示
```
#### 取色图钉
```python
colorpin = Colorpin()                                                        # 创建取色图钉对象
colorpin.connect(colorboard)                                                 # 将取色图钉绑定到取色版上

colorpin.locate(x, y)                                                        # 将图钉定位到取色版坐标(x, y)的位置上 
board_matrix = colorpin.get_cm()                                             # 获取已绘制图钉的取色版计算矩阵
cv2.imshow('color_board_demo', cv2.cvtColor(board_matrix, cv2.COLOR_HSV2BGR) # 将计算矩阵放在窗口上显示
```
#### 取色版API
Colorboard.**connect(bar)** \
绑定已存在的Colorbar对象

Colorboard.**get_current_subcm()** \
获取当前使用中的子计算矩阵,返回值格式为[row, column, color_in_hsv]

Colorboard.**get_subcm(hue)** \
根据色相获得对应的子计算矩阵，返回值格式为[row, column, color_in_hsv]

Colorboard.**get_color(x, y)** \
根据x,y来获取相应OpenCV坐标上的HSV颜色值，返回值的格式为[h, s, v]

Colorboard.**get_color_pos(color_in_hsv)** \
根据HSV颜色值获取其在颜色条以及取色版的位置，返回值格式为[hue, row, column]

#### 取色图钉API

Colorpin.**connect(board)** \
绑定已存在的Colorboard对象

Colorpin.**locate(x, y)** \
在取色版上定位并绘制图钉

Colorpin.**get_cm()** \
获取绘制图钉之后的取色版计算矩阵，返回值格式为[row, column, color_in_hsv]

### 额外配置

参数项 | 含义
--- | ---
use_colorboard_rtcp | 实时计算取色版显示矩阵
use_colorboard_cache | 使用取色版矩阵缓存

### 后续工作
1. ~~加速取色版的色彩显示。在实时计算上优化矩阵计算部分，在缓存机制上优化文件体积~~
2. ~~加入色彩定位~~
3. 添加取色器模块

## 许可证

MIT 许可证