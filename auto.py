import time
import sys
import threading
from ctypes import windll
import tkinter as tk
import winlib
from winlib import get_foreground_window_title, is_key_pressed, press_key, mouse_click

# 鱼类模式
def fishing_mode(hwnd, overlay):
    overlay.update_text("钓鱼模式, 按 A 拉线")
    time.sleep(1)
    while True:
        if is_key_pressed("A"):
            overlay.update_text("拉线中，按 F 退出")
            while not is_key_pressed("F"):
                mouse_click(hwnd, 'right')
                time.sleep(0.005)
            overlay.update_text("钓鱼模式，按 A 拉线")
        elif is_key_pressed("]"):
            overlay.update_text("游戏模式：按 [ 钓鱼，按 : 跳过")
            break
        time.sleep(0.1)

# 跳过模式
def skipping_mode(hwnd, overlay):
    overlay.update_text("跳过模式, 按 F 跳过")
    time.sleep(1)
    while True:
        if is_key_pressed("F"):
            overlay.update_text("跳过中")
            while is_key_pressed("F"):
                press_key(hwnd, "F")
                time.sleep(0.3)
            overlay.update_text("跳过模式, 按 F 跳过")
        elif is_key_pressed("]"):
            overlay.update_text("游戏模式：按 [ 钓鱼，按 : 跳过")
            break
        time.sleep(0.1)

# 跳过模式
def test_mode(hwnd, overlay):
    overlay.update_text("测试模式, 按 F 跳跃")
    time.sleep(1)
    while True:
        if is_key_pressed("F"):
            overlay.update_text("跳跃中")
            while is_key_pressed("F"):
                press_key(hwnd, "SPACE")
                time.sleep(0.3)
            overlay.update_text("测试模式, 按 F 跳过")
        elif is_key_pressed("]"):
            overlay.update_text("游戏模式：按 [ 钓鱼，按 : 跳过")
            break
        time.sleep(0.1)

# 游戏模式
def game_mode(hwnd, overlay):
    overlay.update_text("游戏模式：按 [ 钓鱼，按 : 跳过")
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed("["):
            fishing_mode(hwnd, overlay)
        if is_key_pressed(":"):
            skipping_mode(hwnd, overlay)
        if is_key_pressed("'"):
            test_mode(hwnd, overlay)
        time.sleep(0.1)
    overlay.update_text("退出游戏模式")

# 主要执行函数
def main():

    target_window_title = "无限暖暖"
    overlay = winlib.OverlayWindow()
    overlay_thread = threading.Thread(target=overlay.run, daemon=True)
    overlay_thread.start()
    while True:
        hwnd, active_window = get_foreground_window_title()
        if target_window_title in active_window:
            game_mode(hwnd, overlay)
        time.sleep(1)

if __name__ == "__main__":
    if windll.shell32.IsUserAnAdmin():
        main()
    else:
        windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
