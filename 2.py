import keyboard
import pyautogui
import time

flag=False

def press_win_plus():
    global flag
    if flag==False:
        pyautogui.hotkey('win', '+') 
        flag=True

def press_win_minus():
    global flag
    pyautogui.hotkey('win', '-')
    flag=False

while True:
    if keyboard.is_pressed('shift'): 
        press_win_plus()  
    elif not keyboard.is_pressed('shift'):  
        press_win_minus()  