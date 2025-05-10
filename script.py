import ctypes
from ctypes import wintypes
import keyboard 

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
zoom_level = 1.0  # Start with normal zoom (1.0)
set_zoom_level(zoom_level, 0, 0)
print(f"Magnifier zoom set to {zoom_level * 100}%")

while True:
    if keyboard.is_pressed('shift'):  # Check if '0' key is pressed
        zoom_level = 2  # Set zoom to 400% (or your desired level)
        set_zoom_level(zoom_level, 480, 270)
        print(f"Magnifier zoom set to {zoom_level * 100}%")

    else:
        if zoom_level != 1.0:  # If zoom is not at 100%
            zoom_level = 1.0  # Reset zoom to 100%
            set_zoom_level(zoom_level, 0, 0)
            print(f"Magnifier zoom set to {zoom_level * 100}%")