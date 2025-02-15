import time
import sys
import threading
from ctypes import windll
import tkinter as tk
import winlib
from winlib import get_foreground_window_title, is_key_pressed, press_physical_key

# 跳过模式
def skipping_mode(hwnd, overlay):
    overlay.update_text("跳过模式，按 SPACE 跳过")
    time.sleep(1)
    while True:
        if is_key_pressed("SPACE"):
            overlay.update_text("跳过中，按 ] 退出")
            while is_key_pressed("SPACE"):
                press_physical_key('SPACE')
                time.sleep(0.2)
                press_physical_key("1")
                time.sleep(0.1)
            overlay.update_text("跳过模式，按 SPACE 跳过")
        elif is_key_pressed("]"):
            overlay.update_text("游戏模式")
            break
        time.sleep(0.1)

# 游戏模式
def game_mode(hwnd, overlay):
    overlay.update_text("游戏模式")
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(":"):
            skipping_mode(hwnd, overlay)
        time.sleep(0.1)
    overlay.update_text("退出游戏模式")

# 主要执行函数
def main():

    target_window_title = "绝区零"
    overlay = winlib.OverlayWindow()
    overlay_thread = threading.Thread(target=overlay.run, daemon=True)
    overlay_thread.start()
    while True:
        hwnd, active_window = get_foreground_window_title()
        if target_window_title in active_window:
            game_mode(hwnd, overlay)
        time.sleep(1)

if __name__ == "__main__":
    try:
        if windll.shell32.IsUserAnAdmin():
            main()
        else:
            windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    except Exception as e:
        input(f"Error: {e}\nPress Enter to exit...")