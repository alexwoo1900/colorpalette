# 调色板

用Python和OpenCV编写的调色板工具

README: [ENGLISH](https://github.com/alexwoo1900/colorpalette/blob/master/README.md) | [简体中文](https://github.com/alexwoo1900/colorpalette/blob/master/README_CN.md)

## Demo演示

<div align=center><img src="https://github.com/alexwoo1900/colorpalette/master/docs/assets/colorpalette.gif" alt="colorpalette-usage" /></div>

## 如何使用该工程

### 颜色条

#### 显示颜色条
```python
colorbar = Colorbar(384, 20)                            # 创建颜色条对象
bar_matrix = colorbar.get_matrix()                      # 获取颜色条图像矩阵
cv2.imshow('color_bar_demo', bar_matrix[:, :, ::-1])    # 将图像矩阵放到窗口上显示
```
#### 颜色滑动块
```python
colorstrip = Colorstrip(4, 20)                          # 创建滑动块对象
colorstrip.connect(colorbar)                            # 将滑动块绑定到颜色条上

colorstrip.slide(x)                                     # 让滑动块滑动到x处/在x处绘制
bar_matrix = colorstrip.get_matrix()                    # 获取已绘制滑动块的颜色条图像矩阵
cv2.imshow('color_bar_demo', bar_matrix[:, :, ::-1])    # 将图像矩阵放到窗口上显示
```
#### 颜色条API

Colorbar.**get_matrix()** \
获取颜色条颜色矩阵，格式为[row, column, color]

Colorbar.**get_rgb_by_x(x)** \
根据x值来获取OpenCV坐标x轴上对应位置的RGB颜色值，格式为[r, g, b]

#### 滑动块API

Colorstrip.**connect(bar)** \
绑定已存在的Colorbar对象

Colorstrip.**slide(x)** \
滑动并绘制滑动块到x处

Colorstrip.**get_matrix()** \
获取绘制滑动块后颜色条的颜色矩阵,返回值的格式为[row, column, color]


### 取色版

#### 显示取色版
```python
colorboard = Colorboard(256, 256)                       # 创建取色版对象
colorboard.connect(colorbar)                            # 将取色版绑定到颜色条上

board_matrix = colorboard.get_submatrix_by_index(x)     # 获取取色版需要显示的颜色矩阵
cv2.imshow('color_board_demo', board_matrix[:, :, ::-1])# 将图像矩阵放在窗口上显示
```
#### 取色图钉
```python
colorpin = Colorpin()                                   # 创建取色图钉对象
colorpin.connect(colorboard)                            # 将取色图钉绑定到取色版上

colorpin.locate(x, y)                                   # 将图钉定位到取色版坐标为(x,y)位置上
board_matrix = colorpin.get_matrix()                    # 获取已绘制图钉的取色版图像矩阵
cv2.imshow('color_board_demo', board_matrix[:, :, ::-1])# 将图像矩阵放在窗口上显示
```
#### 取色版API
Colorboard.**connect(bar)** \
绑定已存在的Colorbar对象，取色版会根据Colorbar的色域来创建颜色矩阵

Colorboard.**get_current_submatrix()** \
获取当前使用中的颜色矩阵,返回值格式为[row, column, color]

Colorboard.**get_submatrix_by_index(index)** \
根据索引来获取对应的颜色矩阵，返回值格式同get_current_submatrix

Colorboard.**get_rgb_by_xy(x, y)** \
根据x,y来获取相应OpenCV坐标上的RGB颜色值，返回值的格式为[r, g, b]

#### 取色图钉API

Colorpin.**connect(board)** \
绑定已存在的Colorboard对象

Colorpin.**locate(x, y)** \
在取色版上定位并绘制图钉

Colorpin.**get_matrix()** \
获取绘制图钉之后的取色版颜色矩阵，返回值格式为[row, column, color]

### 额外配置

参数项 | 含义
--- | ---
use_colorboard_rtcp | 实时计算取色版显示矩阵
use_colorboard_cache | 使用取色版矩阵缓存

### 后续工作
1. 加速取色版的色彩显示。在实时计算上优化矩阵计算部分，在缓存机制上优化文件体积
2. 加入色彩定位
3. 添加取色器模块