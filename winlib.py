import ctypes
import time
from ctypes import windll
import tkinter as tk

# 按键代码定义
def vk_codes(name):
    codes = {
        "LBUTTON": 0x01,
        "RBUTTON": 0x02,
        "A": 0x41,
        "F": 0x46,
        ":": 0xBA,
        "[": 0xDB,
        "]": 0xDD,
        "SPACE": 0x20,
    }

    return codes[name]

# 获取当前前台窗口标题
def get_foreground_window_title():
    hwnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hwnd)
    buffer = ctypes.create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
    return hwnd, buffer.value

# 检测按键是否被按下
def is_key_pressed(keyname):
    vk_code = vk_codes(keyname)
    return bool(windll.user32.GetAsyncKeyState(vk_code) & 0x8000)

# 模拟鼠标点击
def left_click(hwnd):
    vk_code = vk_codes("LBUTTON")
    windll.user32.PostMessageW(hwnd, 0x0201, vk_code, build_lparam(vk_code, is_keyup=False))
    time.sleep(0.005)
    windll.user32.PostMessageW(hwnd, 0x0202, vk_code, build_lparam(vk_code, is_keyup=True))
def right_click(hwnd):
    vk_code = vk_codes("RBUTTON")
    windll.user32.PostMessageW(hwnd, 0x0204, vk_code, build_lparam(vk_code, is_keyup=False))
    time.sleep(0.005)
    windll.user32.PostMessageW(hwnd, 0x0205, vk_code, build_lparam(vk_code, is_keyup=True))

def send_right_click_old(hwnd):
    windll.user32.PostMessageW(hwnd, 0x0204, 0, 0)
    time.sleep(0.005)
    windll.user32.PostMessageW(hwnd, 0x0205, 0, 0)

def build_lparam(vk_code, is_keyup=False):
    scancode = windll.user32.MapVirtualKeyW(vk_code, 0)
    if is_keyup:
        return (scancode << 16) | (1 << 30) | (1 << 31)
    else:
        return scancode << 16

# 模拟按键按下
def press_key(hwnd, keyname):
    vk_code = vk_codes(keyname)
    windll.user32.PostMessageW(hwnd, 0x0100, vk_code, build_lparam(vk_code, is_keyup=False))
    time.sleep(0.05)
    windll.user32.PostMessageW(hwnd, 0x0101, vk_code, build_lparam(vk_code, is_keyup=True))

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
