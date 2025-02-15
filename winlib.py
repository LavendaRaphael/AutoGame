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
        ":": 0xBA,
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

def mouse_click(hwnd, leftright, x=100, y=100):
    print(f"Clicking {leftright}")
    lparam = (y << 16) | x
    windll.user32.PostMessageW(hwnd, 0x0200, 0, lparam)  # WM_MOUSEMOVE
    if leftright == "left":
        msg_down = 0x0201
        msg_up = 0x0202
    else:
        msg_down = 0x0204
        msg_up = 0x0205
    windll.user32.PostMessageW(hwnd, msg_up, 0, lparam)  # WM_RBUTTONDOWN
    time.sleep(0.05)
    windll.user32.PostMessageW(hwnd, msg_down, 0, lparam)  # WM_RBUTTONUP

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

def send_key_event(vk_code=0, scancode=0, flags=0):
    INPUT_KEYBOARD = 1
    input_struct = INPUT()
    input_struct.type = INPUT_KEYBOARD
    input_struct.ki = KEYBDINPUT(
        wVk=vk_code,
        wScan=scancode,
        dwFlags=flags,
        time=0,
        dwExtraInfo=0
    )
    
    # 发送输入
    result = ctypes.windll.user32.SendInput(1, ctypes.byref(input_struct), ctypes.sizeof(input_struct))
    if result != 1:
        error_code = ctypes.windll.kernel32.GetLastError()
        print(f"SendInput失败！错误码: {error_code}")
        return False
    return True

def press_physical_key(keyname):
    #print(f"Pressing {keyname}")
    vk_code = vk_codes(keyname)
    scancode = windll.user32.MapVirtualKeyW(vk_code, 0)

    KEYEVENTF_KEYUP = 0x0002
    KEYEVENTF_SCANCODE = 0x0008
    
    send_key_event(scancode=scancode, flags=KEYEVENTF_SCANCODE)
    time.sleep(0.05)
    send_key_event(scancode=scancode, flags=KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP)

def build_lparam(vk_code, keyupdown):
    scancode = windll.user32.MapVirtualKeyW(vk_code, 0)
    lparam = scancode << 16
    if keyupdown == 'keyup':
        lparam |= 0xC0000000
    else:
        lparam |= 0x00000001
    return lparam

#def build_lparam(vk_code, is_keyup=False):
#    scancode = windll.user32.MapVirtualKeyW(vk_code, 0)
#    if is_keyup:
#        return (scancode << 16) | (1 << 30) | (1 << 31)
#    else:
#        return scancode << 16

def press_key(hwnd, keyname):
    print(f"Pressing {keyname}")
    vk_code = vk_codes(keyname)
    windll.user32.PostMessageW(hwnd, 0x0100, vk_code, build_lparam(vk_code, 'keyup'))
    time.sleep(0.05)
    windll.user32.PostMessageW(hwnd, 0x0101, vk_code, build_lparam(vk_code, 'keydown'))

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
