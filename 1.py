from pynput import mouse
import pyautogui

print('Zoom started.')
toggle_state = False

# Define the callback for right-click events
def on_click(x, y, button, pressed):
    global toggle_state
    if button == mouse.Button.right and pressed:
        toggle_state = not toggle_state
        if toggle_state:
            pyautogui.hotkey('win', '+')  # Press Win and '+'
        else:
            pyautogui.hotkey('win', '-')  # Press Win and '-'

# Listen for mouse events
listener = mouse.Listener(on_click=on_click)    # Initiate listener
                                                # 'mouse.Listener()' reads mouse data and passes it into specified function
listener.start()  # Start the listener
listener.join()   # Set continuous execution