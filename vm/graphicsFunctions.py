import sys
sys.path.append('../libs/graphics')
from graphics import *
import time

_window = None
_drawcolor = color_rgb(255, 255, 255)
_bgcolor = color_rgb(0, 0, 0)
_scaleFactor = 1
_dimensions = None
_pixelMatrix = None


def inBounds(position):
    #print(position)
    if position[0] < 0 or position[0] >= _dimensions[0]:
        return False
    if position[1] < 0 or position[1] >= _dimensions[1]:
        return False
    return True

########################


def setbgcolor(memoryManager, paramsList):
    """sets the background color of the window to be used in the next clear call

    parameters
    ----------
    paramsList: the list of parameters given to the function
    memoryManager: the manager of memory of the whole program

    returns
    -------
    empty list.
    """
    global _window
    global _bgcolor

    color = paramsList[0]
    _bgcolor = color_rgb(int(color[0]), int(color[1]), int(color[2]))
    _window.setBackground(_bgcolor)
    return []

def setdrawcolor(memoryManager, paramsList):
    """sets the drawing color of the window to be used in the next pixel call

    parameters
    ----------
    paramsList: the list of parameters given to the function
    memoryManager: the manager of memory of the whole program

    returns
    -------
    empty list.
    """
    global _window
    global _drawcolor

    color = paramsList[0]
    _drawcolor = color_rgb(int(color[0]), int(color[1]), int(color[2]))
    return []

def clear(memoryManager, paramsList):
    """resets the background to the backgroun color of the window

    parameters
    ----------
    paramsList: the list of parameters given to the function
    memoryManager: the manager of memory of the whole program

    returns
    -------
    empty list.
    """
    global _window
    global _drawcolor
    global _pixelMatrix
    global _dimensions

    _pixelMatrix = [[False for x in range(int(_dimensions[0]))] for y in range(int(_dimensions[1]))]
    
    bgFig = Rectangle(Point(-1, -1), Point(_dimensions[0] * _scaleFactor, _dimensions[1] * _scaleFactor))
    bgFig.setFill(_bgcolor)
    bgFig.draw(_window)
    return []
    
def pixel(memoryManager, paramsList):
    """sets a single pixel by coloring it with the draw color

    parameters
    ----------
    paramsList: the list of parameters given to the function
    memoryManager: the manager of memory of the whole program

    returns
    -------
    empty list.
    """
    global _window
    global _drawcolor
    global _scaleFactor
    global _pixelMatrix

    #print(paramsList)
    #position = paramsList[0]
    x = paramsList[0]
    y = paramsList[1]
    if type(x) is tuple:
        x = x[0]
    if type(y) is tuple:
        y = y[0]

    #print("set: ", x, y)
    if not inBounds([x, y]):
        return []

    origin = Point(int(x * _scaleFactor), int(y * _scaleFactor))
    _pixelMatrix[int(y)][int(x)] = True

    pointFig = None
    if _scaleFactor > 1:
        #origin = Point(int(origin.getX() - (_scaleFactor/2)), int(origin.getY() - (_scaleFactor/2)))
        end = Point(origin.getX() + _scaleFactor - 1, origin.getY() + _scaleFactor - 1)

        pointFig = Rectangle(origin, end)
        pointFig.setFill(_drawcolor)
    else:
        pointFig = origin
    
    pointFig.setOutline(_drawcolor)     
    pointFig.draw(_window)
    return []

def getpixel(memoryManager, paramsList):
    """returns if a pixel at position [(x,), (y,)] had been set

    parameters
    ----------
    paramsList: the list of parameters given to the function
    memoryManager: the manager of memory of the whole program

    returns
    -------
    [0.0] if the pixel is not set, else [1.0]
    """
    global _window
    global _drawcolor
    global _scaleFactor
    global _pixelMatrix
    global _dimensions

    #position = paramsList[0]
    x = paramsList[0]
    y = paramsList[1]
    if type(x) is tuple:
        x = x[0]
    if type(y) is tuple:
        y = y[0]

    #print("get: ", x, y)
    if not inBounds([x, y]):
        return [0.0]

    value = _pixelMatrix[int(y)][int(x)]
    #print("got: ", value)
    if value:
        return [1.0]
    else:
        return [0.0]

def createwindow(memoryManager, paramsList):
    """create a new graphics window with agiven resolution, bg color and scale

    parameters
    ----------
    paramsList: the list of parameters given to the function
    memoryManager: the manager of memory of the whole program

    returns
    -------
    empty list.
    """
    global _window
    global _drawcolor
    global _scaleFactor
    global _bgcolor
    global _pixelMatrix
    global _dimensions

    _dimensions = paramsList[0]
    color = paramsList[1]
    scale = paramsList[2]

    if type(scale) is tuple and len(scale) > 0:
        _scaleFactor = scale[0] 
    else:
        _scaleFactor = scale
    
    if _scaleFactor <= 0:
        _scaleFactor = 1

    _pixelMatrix = [[False for x in range(int(_dimensions[0]))] for y in range(int(_dimensions[1]))]
    
    #set bg and create the window
    _bgcolor = color_rgb(int(color[0]), int(color[1]), int(color[2]))
    _drawcolor = color_rgb(255, 255, 255)

    _window = GraphWin("VECING-Lang", int(_dimensions[0] * _scaleFactor), int(_dimensions[1] * _scaleFactor))
    _window.setBackground(_bgcolor) #0 t0 255

    clear(None, None)
    return []
    
    
def stopRender(memoryManager, paramsList):
    """waits for the drawing function calls to finish and closes the window 
        on click from the user

    parameters
    ----------
    paramsList: the list of parameters given to the function
    memoryManager: the manager of memory of the whole program

    returns
    -------
    empty list.
    """
    _window.getMouse()
    time.sleep(0.2)
    _window.close()
    return []

def pause(memoryManager, paramsList):
    """waits for the drawing function calls to finish and continues execution 
        on click from the user

    parameters
    ----------
    paramsList: the list of parameters given to the function
    memoryManager: the manager of memory of the whole program

    returns
    -------
    empty list.
    """
    _window.getMouse()
    time.sleep(0.2)
    # if paramsList is not None and len(paramsList) is not 0:
    #     return paramsList[0]
    return []


# pixel(None, [(20.0, 0.0)])
# for i in range(0, 22):
    
#     for j in range(0, 41):
#         #print(i, j)
#         left = bool(getpixel(None, [(j - 1, i)])[0])
#         center = bool(getpixel(None, [(j, i)])[0])
#         right = bool(getpixel(None, [(j + 1, i)])[0])
#         orCond = center or right

#         result = (left and not orCond) or (not left and orCond)
#         if result:
#             pixel(None, [(j, i + 1)])
    
    
# stopRender(None, None)
