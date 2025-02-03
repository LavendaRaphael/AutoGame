import ctypes
import time
import sys
import logging
import threading
from ctypes import windll
import tkinter as tk
import winlib
from winlib import vk_code, get_foreground_window_title, is_key_pressed, press_key

# 跳过模式
def skipping_mode(hwnd, overlay):
    overlay.update_text("跳过模式")
    time.sleep(1)
    while True:
        if is_key_pressed(vk_code("SPACE")):
            overlay.update_text("跳过中...")
            while is_key_pressed(vk_code("SPACE")):
                press_key(hwnd, vk_code("SPACE"))
                time.sleep(0.3)
            overlay.update_text("跳过模式")
        elif is_key_pressed(vk_code("]")):
            overlay.update_text("退出跳过模式")
            break
        time.sleep(0.1)

# 游戏模式
def game_mode(hwnd, overlay):
    overlay.update_text("游戏模式")
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(vk_code(":")):
            skipping_mode(hwnd, overlay)
        time.sleep(0.1)
    overlay.update_text("退出游戏模式")

# 主要执行函数
def main():

    target_window_title = "MuMu模拟器12"
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