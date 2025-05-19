import ctypes
from ctypes import wintypes
import keyboard

def test_gamma_contrast_set(gamma_value, contrast_value):
    gdi32 = ctypes.windll.gdi32
    user32 = ctypes.windll.user32
    ramp = (ctypes.c_ushort * 256 * 3)()
    
    # Adjust contrast
    for i in range(256):
        # Apply contrast: This formula adjusts contrast by scaling the pixel values.
        # The contrast_value is expected to be between 0 and 1, where 1 means no change.
        contrast_adjusted = int(((i / 255.0 - 0.5) * contrast_value + 0.5) * 255)
        contrast_adjusted = max(0, min(255, contrast_adjusted))  # Clamping to the valid range
        
        # Apply gamma correction after contrast adjustment
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

def set_mouse_sensitivity(sensitivity: int):
    user32 = ctypes.windll.user32
    # Retrieve the current mouse settings
    SPI_SETMOUSESPEED = 113
    # Set the new mouse speed
    success = user32.SystemParametersInfoA(SPI_SETMOUSESPEED, 0, ctypes.c_int(sensitivity), 0)
    if success:
        print(f"Sensivity: {sensitivity}.")
    else:
        print("Failed to set mouse sensitivity.")

# Example usage:
gamma = 1  # Typical gamma value
contrast = 1  # Slight contrast increase (1.0 means no change, values > 1 increase contrast)
desired_sensitivity = 20 # Windows cursor sensivity (1 to 20)
set_mouse_sensitivity(desired_sensitivity)
if not test_gamma_contrast_set(gamma, contrast):
    print("Gamma and contrast adjustment test failed.")