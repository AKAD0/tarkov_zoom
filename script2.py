import ctypes
from ctypes import wintypes
import keyboard
import time

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

def set_contrast(contrast_value):
    """
    Adjust screen contrast by simulating contrast changes using gamma ramp.
    :param contrast_value: Contrast adjustment factor (1.0 = normal, >1.0 = higher contrast, <1.0 = lower contrast)
    """
    # Initialize the gamma ramp
    ramp = (ctypes.c_ushort * 256 * 3)()
    for i in range(256):
        value = max(0, min(255, int((i - 128) * contrast_value + 128)))  # Scale values for contrast
        value = int(value / 255.0 * 65535)  # Convert to 16-bit range
        ramp[0][i] = ramp[1][i] = ramp[2][i] = value

    # Get the device context for the screen
    hdc = ctypes.windll.user32.GetDC(0)
    if hdc == 0:
        raise RuntimeError("Failed to get device context.")

    # Apply the gamma ramp
    if not ctypes.windll.gdi32.SetDeviceGammaRamp(hdc, ctypes.byref(ramp)):
        raise RuntimeError("Failed to set gamma ramp.")
    ctypes.windll.user32.ReleaseDC(0, hdc)

    print(f"Contrast set to: {contrast_value}")


gamma = int(3)
if not test_gamma_set(gamma):
    print("Gamma adjustment test failed.")
set_contrast(1.5)


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
pause = 0.1

while True:
    if keyboard.is_pressed('shift'): 
        if press_start_time is None:
            press_start_time = time.time()

        if time.time() - press_start_time >= pause:
            zoom_level = 3
            x = int(960*((16-(16/zoom_level))/16))
            y = int((x/16)*9)
            set_zoom_level(zoom_level, x, y)

    else:
        press_start_time = None
        if zoom_level != 1.0:  
            zoom_level = 1.0  
            set_zoom_level(zoom_level, 0, 0)