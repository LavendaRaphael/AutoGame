import ctypes
import time
from ctypes import windll
import tkinter as tk
from ctypes import wintypes

# 按键代码定义
def vk_codes(name):
    codes = {
        "LBUTTON": 0x01,
        "RBUTTON": 0x02,
        "1": 0x31,
        "A": 0x41,
        "E": 0x45,
        "F": 0x46,
        ";": 0xBA,
        "[": 0xDB,
        "]": 0xDD,
        "'": 0xDE,
        "SPACE": 0x20,
    }

    return codes[name]

def get_foreground_window_title():
    hwnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hwnd)
    buffer = ctypes.create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hwnd, buffer, length + 1)
    return hwnd, buffer.value

def is_key_pressed(keyname):
    vk_code = vk_codes(keyname)
    return bool(windll.user32.GetAsyncKeyState(vk_code) & 0x8000)

# 根据系统架构定义 ULONG_PTR
if ctypes.sizeof(ctypes.c_void_p) == 8:
    ULONG_PTR = ctypes.c_ulonglong
else:
    ULONG_PTR = ctypes.c_ulong

# 修复结构体内存对齐
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]

class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]

class INPUT(ctypes.Structure):
    _anonymous_ = ("_union",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("_union", INPUT_UNION),
    ]

def press_physical_key(keyname):
    vk_code = vk_codes(keyname)
    scancode = windll.user32.MapVirtualKeyW(vk_code, 0)

    KEYEVENTF_KEYUP = 0x0002
    KEYEVENTF_SCANCODE = 0x0008
    input_struct = INPUT()
    input_struct.type = 1
    input_struct.ki = KEYBDINPUT(
        wVk=0,
        wScan=scancode,
        dwFlags=KEYEVENTF_SCANCODE,
        time=0,
        dwExtraInfo=0
    )
    
    # 发送输入
    windll.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(input_struct))
    time.sleep(0.05)
    input_struct.ki.dwFlags = KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP
    windll.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(input_struct))

def click_mouse(button, position=None):
    
    if position is not None:
        windll.user32.SetCursorPos(position[0], position[1])

    """独立鼠标点击函数"""

    # 鼠标事件标志常量
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004
    MOUSEEVENTF_RIGHTDOWN = 0x0008
    MOUSEEVENTF_RIGHTUP = 0x0010
    MOUSEEVENTF_MIDDLEDOWN = 0x0020
    MOUSEEVENTF_MIDDLEUP = 0x0040
    button_map = {
        "MOUSELEFT": (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP),
        "MOUSERIGHT": (MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP),
        "MOUSEMIDDLE": (MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP),
    }
    
    flags = button_map[button]
    
    # 发送按下事件
    input_struct = INPUT()
    input_struct.type = 0  # INPUT_MOUSE
    input_struct.mi = MOUSEINPUT(
        dwFlags=flags[0],
        mouseData=0,
        time=0,
        dwExtraInfo=0
    )
    windll.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(input_struct))
    time.sleep(0.05)  # 保持按下状态
    input_struct.mi.dwFlags = flags[1]
    windll.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(input_struct))

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

        self.root.geometry(f"1000x100+0+{screen_height-100}")

        self.label = tk.Label(self.root, text="启动", font=("SimHei", 12, "bold"), fg="white", bg="black", anchor="w")
        self.label.pack(fill=tk.BOTH, expand=True)

    def update_text(self, text):
        self.label.config(text=text)  # 更新显示的内容
        self.root.update()

    def run(self):
        self.root.mainloop()
