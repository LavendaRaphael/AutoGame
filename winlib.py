import ctypes
import time
import tkinter as tk
from ctypes import windll,wintypes,create_unicode_buffer,byref, c_ubyte
import numpy as np
import cv2
from PIL import Image, ImageTk

class LogOverlay:
    def __init__(self, master):
        self.root = tk.Toplevel(master)
        self.root.title("Overlay")
        self.root.attributes("-topmost", True)  # 确保窗口始终在最前面
        self.root.attributes("-transparentcolor", "black")  # 设置透明色为黑色
        self.root.overrideredirect(True)

        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.geometry(f"1000x100+0+{screen_height-100}")

        self.label = tk.Label(self.root, text="启动", font=("SimHei", 12, "bold"), fg="white", bg="black", anchor="w")
        self.label.pack(fill=tk.BOTH, expand=True)

    def update_text(self, text):
        self.label.config(text=text)  # 更新显示的内容
        self.root.update()

    #def update(self):
    #    self.root.update_idletasks()
    #    self.root.update()

class PicOverlay:
    def __init__(self, master):
        self.root = tk.Toplevel(master)
        self.root.wm_attributes("-topmost", True)  # 置顶
        self.root.wm_attributes("-transparentcolor", "black")
        self.root.overrideredirect(True)  # 无边框
        
        # 初始位置（右上角）
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry("300x200+{}+10".format(self.screen_width-310))
        
        init_img = np.zeros((200,300,4), dtype=np.uint8)
        img_pil = Image.fromarray(cv2.cvtColor(init_img, cv2.COLOR_BGRA2RGBA))
        img_tk = ImageTk.PhotoImage(image=img_pil)

        self.label = tk.Label(self.root, image=img_tk, bg="black")
        self.label.pack()
        
    def update_overlay(self, overlay_image):
        if overlay_image is not None:
            # 将OpenCV图像转换为PIL格式
            overlay_image = cv2.cvtColor(overlay_image, cv2.COLOR_BGRA2RGBA)
            img_pil = Image.fromarray(overlay_image)
            img_tk = ImageTk.PhotoImage(image=img_pil)
            
            self.label.configure(image=img_tk)
            self.label.image = img_tk  # 保持引用
            
            h, w = overlay_image.shape[:2]
            self.root.geometry(f"{w}x{h}+0+0")
            self.root.update()
    
    #def update(self):
    #    self.root.update_idletasks()
    #    self.root.update()

def find_pic(hwnd, pic, pic_overlay, debug=False):
    image = capture(hwnd)
    value, loc, debug_overlay = match_pic(image, pic)
    #print(hwnd,pic,value, loc)
    #if value > 0.95:
    if True:
        if debug:
            pic_overlay.update_overlay(debug_overlay)
        return True, loc
    else:
        return False, None

def capture(hwnd: wintypes.HWND):
    #windll.user32.SetProcessDPIAware()
    
    # 获取窗口尺寸
    r = wintypes.RECT()
    windll.user32.GetClientRect(hwnd, byref(r))
    width, height = r.right, r.bottom
    
    # 创建兼容DC
    dc = windll.user32.GetDC(hwnd)
    cdc = windll.gdi32.CreateCompatibleDC(dc)
    bitmap = windll.gdi32.CreateCompatibleBitmap(dc, width, height)
    windll.gdi32.SelectObject(cdc, bitmap)
    
    # 关键修改：使用 PrintWindow 替代 BitBlt
    PW_RENDERFULLCONTENT = 0x02
    windll.user32.PrintWindow(hwnd, cdc, PW_RENDERFULLCONTENT)
    
    # 获取位图数据
    total_bytes = width * height * 4
    buffer = bytearray(total_bytes)
    byte_array = (ctypes.c_ubyte * total_bytes).from_buffer(buffer)
    windll.gdi32.GetBitmapBits(bitmap, total_bytes, byte_array)
    
    # 清理资源
    windll.gdi32.DeleteObject(bitmap)
    windll.gdi32.DeleteObject(cdc)
    windll.user32.ReleaseDC(hwnd, dc)
    
    return np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)

def capture_bitblt(hwnd: wintypes.HWND):
    
    # 排除缩放干扰
    windll.user32.SetProcessDPIAware()

    r = wintypes.RECT()
    windll.user32.GetClientRect(hwnd, byref(r))
    width, height = r.right, r.bottom

    dc = windll.user32.GetDC(hwnd)
    cdc = windll.gdi32.CreateCompatibleDC(dc)
    bitmap = windll.gdi32.CreateCompatibleBitmap(dc, width, height)
    windll.gdi32.SelectObject(cdc, bitmap)
    SRCCOPY = 0x00CC0020
    windll.gdi32.BitBlt(cdc, 0, 0, width, height, dc, 0, 0, SRCCOPY)

    total_bytes = width*height*4
    buffer = bytearray(total_bytes)
    byte_array = c_ubyte*total_bytes
    windll.gdi32.GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
    windll.gdi32.DeleteObject(bitmap)
    windll.gdi32.DeleteObject(cdc)
    windll.user32.ReleaseDC(hwnd, dc)

    return np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)

def match_pic(image, pic):

    gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
    target = cv2.imread(pic, cv2.IMREAD_UNCHANGED)
    template = cv2.cvtColor(target, cv2.COLOR_BGRA2GRAY)
    alpha = None
    if target.shape[2] == 4 and np.any(target[:, :, 3] < 255):
        alpha = target[:,:,3]
    
    result = cv2.matchTemplate(gray, template, cv2.TM_CCORR_NORMED, mask=alpha)
    #result = cv2.matchTemplate(gray, template, cv2.TM_SQDIFF, mask=alpha)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    h, w = template.shape[:2]
    loc = max_loc
    val = max_val
    center_x = loc[0] + w // 2
    center_y = loc[1] + h // 2
    
    debug_overlay = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)
    cv2.rectangle(debug_overlay, loc, (loc[0] + w, loc[1] + h), (0, 0, 255, 180), 2)
    cv2.circle(debug_overlay, (center_x, center_y), 5, (0, 255, 0, 200), -1)
    cv2.putText(debug_overlay, f"{pic} {val:.3f}", (loc[0], loc[1] - 10), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(debug_overlay, f"({center_x}, {center_y})", (loc[0], loc[1] + h + 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255, 255), 1, cv2.LINE_AA)
    #cv2.imwrite(f"debug_frame_{int(time.time())}.png", overlay)
    return val, (center_x, center_y), debug_overlay

def get_allwindows():
    user32 = windll.user32
    EnumWindows = user32.EnumWindows
    EnumWindowsProc = wintypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    IsWindowVisible = user32.IsWindowVisible
    GetWindowTextLengthW = user32.GetWindowTextLengthW
    GetWindowTextW = user32.GetWindowTextW

    windows = []

    def callback(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLengthW(hwnd)
            if length > 0:
                buffer = create_unicode_buffer(length + 1)
                GetWindowTextW(hwnd, buffer, length + 1)
                windows.append((hwnd, buffer.value))
        return True

    EnumWindows(EnumWindowsProc(callback), 0)
    return windows

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

def press(keyname, position=None):
    
    if 'MOUSE' in keyname:
        click_mouse(keyname, position)
    else:
        press_physical_key(keyname)

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
