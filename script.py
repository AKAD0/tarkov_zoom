import ctypes
from ctypes import wintypes
import keyboard


print('Setting gamma...')

def test_gamma_set(gamma_value):
    gdi32 = ctypes.windll.gdi32
    user32 = ctypes.windll.user32

    ramp = (ctypes.c_ushort * 256 * 3)()
    for i in range(256):
        value = int((i / 255.0) ** (1.0 / gamma_value) * 65535)
        ramp[0][i] = ramp[1][i] = ramp[2][i] = min(value, 65535)

    hdc = user32.GetDC(0)
    if hdc == 0:
        print("Failed to get device context.")
        return False

    success = gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(ramp))
    user32.ReleaseDC(0, hdc)

    if not success:
        print("SetDeviceGammaRamp failed.")
        return False

    print(f"Gamma successfully set to {gamma_value}.")
    return True

# Test the gamma adjustment
gamma = int(3)
if not test_gamma_set(gamma):
    print("Gamma adjustment test failed.")



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
    if keyboard.is_pressed('shift'):  
        zoom_level = 2  
        set_zoom_level(zoom_level, 480, 270)

    else:
        if zoom_level != 1.0:  
            zoom_level = 1.0  
            set_zoom_level(zoom_level, 0, 0)