import ctypes
from ctypes import wintypes
import keyboard
import time


def test_gamma_contrast_set(gamma_value, contrast_value):
    gdi32 = ctypes.windll.gdi32
    user32 = ctypes.windll.user32
    ramp = (ctypes.c_ushort * 256 * 3)()
    
    # Adjust contrast
    for i in range(256):
        contrast_adjusted = int(((i / 255.0 - 0.5) * contrast_value + 0.5) * 255)
        contrast_adjusted = max(0, min(255, contrast_adjusted))  # Clamping to the valid range
        
        value = int((contrast_adjusted / 255.0) ** (1.0 / gamma_value) * 65535)
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
    print(f"Gamma successfully set to {gamma_value}, Contrast successfully set to {contrast_value}.")
    return True


gamma = 4           # 1.0 = no change
contrast = 1.05     # 1.0 = no change
if not test_gamma_contrast_set(gamma, contrast):
    print("Gamma and contrast adjustment test failed.")





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
press_start_time = None
pause = 0

while True:
    if keyboard.is_pressed('shift'): 
        if press_start_time is None:
            press_start_time = time.time()

        if time.time() - press_start_time >= pause:
            zoom_level = 4
            x = int(960*((16-(16/zoom_level))/16))
            y = int((x/16)*9)
            set_zoom_level(zoom_level, x, y)

    else:
        press_start_time = None
        if zoom_level != 1.0:  
            zoom_level = 1.0  
            set_zoom_level(zoom_level, 0, 0)