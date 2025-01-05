import ctypes
from ctypes import windll
import time
import sys

def get_foreground_window_title():
    hwnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hwnd)
    buffer = ctypes.create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
    return hwnd, buffer.value

def is_key_pressed(vk_code):
    return bool(windll.user32.GetAsyncKeyState(vk_code) & 0x8000)

def send_right_click(hwnd):
    windll.user32.PostMessageW(hwnd, 0x0204, 0, 0)
    time.sleep(0.005)
    windll.user32.PostMessageW(hwnd, 0x0205, 0, 0)

def fishing_mode(hwnd):
    print("fishing mode")
    time.sleep(1)
    while True:
        if is_key_pressed(0x41):
            print("fishing")
            while True:
                send_right_click(hwnd)
                time.sleep(0.005)
                if is_key_pressed(0x46):
                    print("fishing end")
                    break
        elif is_key_pressed(0xDB):
            print("fishing mode exit")
            break
        time.sleep(0.1)

def game_mode(hwnd):
    print("game mode")
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(0xDB):
            fishing_mode(hwnd)
        time.sleep(0.1)
    print("game mode exit")
def monitor(target_window_title):
    while True:
        hwnd, active_window = get_foreground_window_title()
        if target_window_title in active_window:
            game_mode(hwnd)
        time.sleep(1)

if __name__ == "__main__":   
    if not windll.shell32.IsUserAnAdmin():
        windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    target_window_title = "无限暖暖"
    monitor(target_window_title)
    
