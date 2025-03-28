import time
import sys
import threading
from ctypes import windll
import tkinter as tk
import winlib
from winlib import get_foreground_window_title, is_key_pressed, click_mouse, press_physical_key

# 鱼类模式
def fishing_mode(overlay):
    overlay.update_text("钓鱼模式, 按 A 拉线")
    time.sleep(1)
    while True:
        if is_key_pressed("A"):
            overlay.update_text("拉线中，按 F 退出")
            while not is_key_pressed("F"):
                click_mouse('right')
                time.sleep(0.1)
            overlay.update_text("钓鱼模式，按 A 拉线")
        elif is_key_pressed("]"):
            break
        time.sleep(0.1)

# 跳过模式
def skipping_mode(overlay):
    overlay.update_text("跳过模式, 按 SPACE 跳过")
    time.sleep(1)
    while True:
        if is_key_pressed("SPACE"):
            overlay.update_text("跳过中")
            while is_key_pressed("SPACE"):
                click_mouse("left")
                time.sleep(0.1)
                press_physical_key("1")
                time.sleep(0.1)
            overlay.update_text("跳过模式, 按 SPACE 跳过")
        elif is_key_pressed("]"):
            break
        time.sleep(0.1)

# 游戏模式
def game_mode(hwnd, overlay, active_window):
    overlay.update_text(f"{active_window} [ 钓鱼 : 跳过")
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed("["):
            fishing_mode(overlay)
            overlay.update_text(f"{active_window} [ 钓鱼 : 跳过")
        if is_key_pressed(":"):
            skipping_mode( overlay)
            overlay.update_text(f"{active_window} [ 钓鱼 : 跳过")
        time.sleep(0.1)
    overlay.update_text("退出游戏模式")

# 主要执行函数
def main():

    overlay = winlib.OverlayWindow()
    overlay_thread = threading.Thread(target=overlay.run, daemon=True)
    overlay_thread.start()
    overlay.update_text("启动")
    while True:
        hwnd, active_window = get_foreground_window_title()
        if is_key_pressed("]"):
            game_mode(hwnd, overlay, active_window)
        time.sleep(1)

if __name__ == "__main__":
    if windll.shell32.IsUserAnAdmin():
        main()
    else:
        windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
