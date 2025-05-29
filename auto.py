import time
import sys
import threading
from ctypes import windll
import tkinter as tk
import winlib
from winlib import get_foreground_window_title, is_key_pressed, click_mouse, press_physical_key
import logging
import cv2
import pyautogui
import numpy as np

# 配置日志记录
logging.basicConfig(
    filename='debug.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
# 鱼类模式
def fishing(overlay):
    overlay.update_text("钓鱼模式, 按 A 拉线")
    time.sleep(1)
    while True:
        if is_key_pressed("A"):
            overlay.update_text("拉线中，按 F 退出")
            while not is_key_pressed("F"):
                click_mouse('MOUSERIGHT')
                time.sleep(0.1)
            overlay.update_text("钓鱼模式，按 A 拉线")
        elif is_key_pressed("]"):
            break
        time.sleep(0.1)

# 跳过模式
def skipping(overlay, skip_key):
    overlay.update_text("跳过模式, 按 SPACE 跳过")
    time.sleep(1)
    while True:
        if is_key_pressed("SPACE"):
            overlay.update_text("跳过中")
            while is_key_pressed("SPACE"):
                if 'MOUSE' in skip_key:
                    click_mouse(skip_key)
                else:
                    press_physical_key(skip_key)
                time.sleep(0.1)
                press_physical_key("1")
                time.sleep(0.1)
            overlay.update_text("跳过模式, 按 SPACE 跳过")
        elif is_key_pressed("]"):
            break
        time.sleep(0.1)

# 游戏模式
def nikky(hwnd, overlay, active_window):
    overlay.update_text(f"{active_window} [ 钓鱼 : 跳过")
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed("["):
            fishing(overlay)
            overlay.update_text(f"{active_window} [ 钓鱼 : 跳过")
        elif is_key_pressed(":"):
            skipping(overlay, skip_key='F')
            overlay.update_text(f"{active_window} [ 钓鱼 : 跳过")
        time.sleep(0.1)
    overlay.update_text("退出游戏模式")

def rush(overlay):

    overlay.update_text("刷本中 ] 退出")
    time.sleep(1)
    while True:
        if is_key_pressed("]"):
            break
        click_mouse('MOUSELEFT')#, (1800, 1600))
        time.sleep(1)

def rush2():

    # 读取模板图像
    template = cv2.imread('.\再来一次.png', 0)
    print(template)
    w, h = template.shape[::-1]

    # 截图并转换为灰度
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # 匹配模板
    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.8)
    print(loc)

def mihoyo(hwnd, overlay, active_window):
    function = f"{active_window} : 跳过 [ 刷本"
    overlay.update_text(function)
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(":"):
            skipping(overlay, skip_key='MOUSELEFT')
            overlay.update_text(function)
        if is_key_pressed("["):
            rush(overlay)
            overlay.update_text(function)
        time.sleep(0.1)
    overlay.update_text("退出游戏模式")

# 主要执行函数
def game_script_thread(overlay):
    
    while True:
        hwnd, active_window = get_foreground_window_title()
        if active_window == "无限暖暖  ":
            nikky(hwnd, overlay, active_window)
        elif active_window in ["崩坏：星穹铁道","绝区零", '重返未来：1999']:
            mihoyo(hwnd, overlay, active_window)
        else:
            logging.info(f"当前窗口: {active_window}，不在游戏中")
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