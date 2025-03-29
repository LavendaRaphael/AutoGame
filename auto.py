import time
import sys
import threading
from ctypes import windll
import tkinter as tk
import winlib
from winlib import get_foreground_window_title, is_key_pressed, click_mouse, press_physical_key
import logging

# 配置日志记录
logging.basicConfig(
    filename='debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
# 鱼类模式
def fishing(overlay):
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
def skipping(overlay, mode='mouse'):
    overlay.update_text("跳过模式, 按 SPACE 跳过")
    time.sleep(1)
    while True:
        if is_key_pressed("SPACE"):
            overlay.update_text("跳过中")
            while is_key_pressed("SPACE"):
                if mode == 'mouse':
                    click_mouse("left")
                    time.sleep(0.1)
                    press_physical_key("1")
                else:
                    press_physical_key("F")
                time.sleep(0.1)
            overlay.update_text("跳过模式, 按 SPACE 跳过")
        elif is_key_pressed("]"):
            break
        time.sleep(0.1)

# 游戏模式
def game_mode(hwnd, overlay, active_window, skipping_mode='mouse'):
    overlay.update_text(f"{active_window} [ 钓鱼 : 跳过")
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed("["):
            fishing(overlay)
            overlay.update_text(f"{active_window} [ 钓鱼 : 跳过")
        elif is_key_pressed(":"):
            skipping(overlay, mode=skipping_mode)
            overlay.update_text(f"{active_window} [ 钓鱼 : 跳过")
        time.sleep(0.1)
    overlay.update_text("退出游戏模式")

# 主要执行函数
def game_script_thread(overlay):
    
    while True:
        hwnd, active_window = get_foreground_window_title()
        if active_window == "无限暖暖  ":
            game_mode(hwnd, overlay, active_window, skipping_mode='F')
        elif active_window == "绝区零" or active_window == "崩坏: 星穹铁道":
            game_mode(hwnd, overlay, active_window)
        time.sleep(1)

def main():
    if not windll.shell32.IsUserAnAdmin():
        windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        return

    overlay = winlib.OverlayWindow()
    # 将 overlay 实例传递给子线程
    script_thread = threading.Thread(target=game_script_thread, args=(overlay,), daemon=True)
    script_thread.start()
    overlay.run()

if __name__ == "__main__":
    main()