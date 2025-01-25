import ctypes
import time
import sys
import logging
import threading
from ctypes import windll
import tkinter as tk

# 按键代码定义
vk_code = {
    "A": 0x41,
    "F": 0x46,
    ":": 0xBA,
    "[": 0xDB,
    "]": 0xDD,
    "SPACE": 0x20,
}

# 获取当前前台窗口标题
def get_foreground_window_title():
    hwnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hwnd)
    buffer = ctypes.create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
    return hwnd, buffer.value

# 检测按键是否被按下
def is_key_pressed(vk_code):
    return bool(windll.user32.GetAsyncKeyState(vk_code) & 0x8000)

# 模拟鼠标右键点击
def send_right_click(hwnd):
    windll.user32.PostMessageW(hwnd, 0x0204, 0, 0)
    time.sleep(0.005)
    windll.user32.PostMessageW(hwnd, 0x0205, 0, 0)

# 模拟按键按下
def press_key(hwnd, vk_code):
    windll.user32.PostMessageW(hwnd, 0x0100, vk_code, 0)
    time.sleep(0.05)
    windll.user32.PostMessageW(hwnd, 0x0101, vk_code, 0)

# 创建透明遮罩窗口
class OverlayWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Overlay")
        self.root.attributes("-topmost", True)  # 确保窗口始终在最前面
        self.root.attributes("-transparentcolor", "black")  # 设置透明色为黑色
        self.root.overrideredirect(True)  # 去掉标题栏

        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.geometry(f"200x100+0+{screen_height-100}")

        self.label = tk.Label(self.root, text="启动", font=("SimHei", 12, "bold"), fg="white", bg="black", anchor="w")
        self.label.pack(fill=tk.BOTH, expand=True)

        self.text_buffer = ""  # 用于存储显示的文本

    def update_text(self, text):
        # 更新文本时避免重叠，清空旧内容
        self.text_buffer = text
        self.label.config(text=self.text_buffer)  # 更新显示的内容
        self.root.update()

    def run(self):
        self.root.mainloop()

# 鱼类模式
def fishing_mode(hwnd, overlay):
    overlay.update_text("钓鱼模式")
    time.sleep(1)
    while True:
        if is_key_pressed(vk_code["A"]):
            overlay.update_text("钓鱼中...")
            while not is_key_pressed(vk_code["F"]):
                send_right_click(hwnd)
                time.sleep(0.005)
            overlay.update_text("钓鱼模式")
        elif is_key_pressed(vk_code["]"]):
            overlay.update_text("退出钓鱼模式")
            break
        time.sleep(0.1)

# 跳过模式
def skipping_mode(hwnd, overlay):
    overlay.update_text("跳过模式")
    time.sleep(1)
    while True:
        if is_key_pressed(vk_code["SPACE"]):
            overlay.update_text("跳过中...")
            while is_key_pressed(vk_code["SPACE"]):
                press_key(hwnd, vk_code["F"])
                time.sleep(0.3)
            overlay.update_text("跳过模式")
        elif is_key_pressed(vk_code["]"]):
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
        if is_key_pressed(vk_code["["]):
            fishing_mode(hwnd, overlay)
        if is_key_pressed(vk_code[":"]):
            skipping_mode(hwnd, overlay)
        time.sleep(0.1)
    overlay.update_text("退出游戏模式")

# 主要执行函数
def main():

    target_window_title = "无限暖暖"
    overlay = OverlayWindow()
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
