import ctypes
import time
import sys
import logging
import threading
import queue
from ctypes import windll, wintypes
import tkinter as tk

# 配置日志记录
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# 按键代码定义
vk_code = {
    "A": 0x41,
    "F": 0x46,
    ":": 0xBA,
    "[": 0xDB,
    "]": 0xDD,
    "SPACE": 0x20,
    "1": 0x31,
}

# 定义输入结构
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]

class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("ki", KEYBDINPUT),
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", INPUT_UNION),
    ]

LPINPUT = ctypes.POINTER(INPUT)
ctypes.windll.user32.SendInput.argtypes = (wintypes.UINT, LPINPUT, ctypes.c_int)
ctypes.windll.user32.SendInput.restype = wintypes.UINT

def press_key(vk_code):
    try:
        inputs = (INPUT * 2)()
        inputs[0].type = INPUT_KEYBOARD
        inputs[0].union.ki = KEYBDINPUT(vk_code, 0, 0, 0, None)
        inputs[1].type = INPUT_KEYBOARD
        inputs[1].union.ki = KEYBDINPUT(vk_code, 0, KEYEVENTF_KEYUP, 0, None)
        ctypes.windll.user32.SendInput(2, inputs, ctypes.sizeof(INPUT))
        time.sleep(0.05)
    except Exception as e:
        logging.error("模拟按键失败: %s", e)

# 获取当前前台窗口标题
def get_foreground_window_title():
    try:
        hwnd = windll.user32.GetForegroundWindow()
        length = windll.user32.GetWindowTextLengthW(hwnd)
        buffer = ctypes.create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
        return hwnd, buffer.value
    except Exception as e:
        logging.error("获取窗口信息失败: %s", e)
        return None, ""

# 检测按键状态
def is_key_pressed(vk_code):
    try:
        return bool(windll.user32.GetAsyncKeyState(vk_code) & 0x8000)
    except Exception as e:
        logging.error("检测按键失败: %s", e)
        return False

# 创建透明遮罩窗口
class OverlayWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Overlay")
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black")
        self.root.overrideredirect(True)
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"200x100+10+{screen_height - 110}")  # 右下角偏移10像素

        self.label = tk.Label(self.root, text="启动", font=("SimHei", 12), 
                            fg="white", bg="black", anchor="w")
        self.label.pack(fill=tk.BOTH, expand=True)

        self.queue = queue.Queue()
        self.root.after(100, self.process_queue)

    def process_queue(self):
        try:
            while True:
                msg = self.queue.get_nowait()
                self.label.config(text=msg)
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)

    def update_text(self, text):
        self.queue.put(text)

    def run(self):
        self.root.mainloop()

# 模式处理函数
def skipping_mode(hwnd, overlay):
    overlay.update_text("跳过模式")
    try:
        while True:
            if is_key_pressed(vk_code["F"]):
                overlay.update_text("跳过中...")
                while is_key_pressed(vk_code["F"]):
                    press_key(vk_code["SPACE"])
                    time.sleep(0.8)  # 调整间隔时间
                    press_key(vk_code["1"])
                    time.sleep(0.8)
                overlay.update_text("跳过模式")
            elif is_key_pressed(vk_code["]"]):
                overlay.update_text("退出跳过模式")
                break
            time.sleep(0.1)
    except Exception as e:
        logging.error("跳过模式错误: %s", e)

def game_mode(overlay):
    overlay.update_text("游戏模式")
    try:
        while True:
            hwnd, active_window = get_foreground_window_title()
            if "崩坏：星穹铁道" not in active_window:
                break
            if is_key_pressed(vk_code[":"]):
                skipping_mode(hwnd, overlay)
                overlay.update_text("游戏模式")
            time.sleep(0.1)
    except Exception as e:
        logging.error("游戏模式错误: %s", e)
    overlay.update_text("程序就绪")

# 主逻辑
def main_loop(overlay):
    logging.info("程序启动")
    while True:
        try:
            hwnd, active_window = get_foreground_window_title()
            if "崩坏：星穹铁道" in active_window:
                game_mode(overlay)
            time.sleep(1)
        except KeyboardInterrupt:
            overlay.update_text("程序退出")
            sys.exit()
        except Exception as e:
            logging.error("主循环错误: %s", e)
            time.sleep(1)

if __name__ == "__main__":
    if windll.shell32.IsUserAnAdmin():
        overlay = OverlayWindow()
        threading.Thread(target=main_loop, args=(overlay,), daemon=True).start()
        overlay.run()
    else:
        windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)