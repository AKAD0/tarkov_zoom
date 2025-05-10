import ctypes
from ctypes import wintypes
import keyboard


print('Launching zoom...')
magnification = ctypes.WinDLL('Magnification.dll')
magnification.MagInitialize.restype = wintypes.BOOL
magnification.MagSetFullscreenTransform.argtypes = [wintypes.FLOAT, wintypes.INT, wintypes.INT]
magnification.MagSetFullscreenTransform.restype = wintypes.BOOL

def initialize_magnifier():
    if not magnification.MagInitialize():
        raise RuntimeError("Failed to initialize the magnifier.")

def set_zoom_level(zoom_level, x, y):
    if not magnification.MagSetFullscreenTransform(zoom_level, x, y):
        raise RuntimeError("Failed to set the zoom level.")

initialize_magnifier()
zoom_level = 1.0 
set_zoom_level(zoom_level, 0, 0)
print('Zoom\'s a-go.')


while True:
    if keyboard.is_pressed('alt'):  
        zoom_level = 2  
        set_zoom_level(zoom_level, 480, 270)

    else:
        if zoom_level != 1.0:  
            zoom_level = 1.0  
            set_zoom_level(zoom_level, 0, 0)