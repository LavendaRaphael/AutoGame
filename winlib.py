import ctypes
import time
import tkinter as tk
from ctypes import windll,wintypes,create_unicode_buffer,byref, c_ubyte
import numpy as np
import cv2
from PIL import Image, ImageTk
import logging
from datetime import datetime

def skipping_cv(log_overlay, pic_overlay, hwnd, pic_dict):
    txt = "跳过模式 ] 退出"
    log_overlay.update_text(txt)
    time.sleep(1)
    while True:
        if is_key_pressed("]"):
            pic_overlay.hide_overlay()
            break
        image = capture(hwnd)
        for pic, prop in pic_dict.items():
            picrange = prop['picrange']
            key = prop['key']
            shift = prop['shift']
            #picrange = (0,0,2880,1800)
            tof, loc = find_pic(image, pic, picrange, log_overlay, debug=True, pic_overlay=pic_overlay)
            if tof:
                press(key, (loc[0]+shift[0], loc[1]+shift[1]))
                break
        time.sleep(0.2)
        if not tof:
            log_overlay.update_text(txt)

def fishing(overlay):
    txt = "钓鱼模式, 按 A 拉线"
    overlay.update_text(txt)
    time.sleep(1)
    while True:
        if is_key_pressed("A"):
            overlay.update_text("拉线中 F 退出")
            while not is_key_pressed("F"):
                press('MOUSERIGHT')
                time.sleep(0.1)
            overlay.update_text(txt)
        elif is_key_pressed("]"):
            break
        time.sleep(0.1)
        
def skipping(overlay, skip_key):
    overlay.update_text("跳过模式 ] 退出")
    time.sleep(1)
    while True:
        if is_key_pressed("]"):
            break
        else:
            for keyname in skip_key:
                press(keyname)
            time.sleep(0.2)

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

        self.root.geometry(f"{screen_width}x100+0+{screen_height-100}")

        self.label = tk.Label(self.root, text="启动", font=("SimHei", 12, "bold"), fg="white", bg="black", anchor="w")
        self.label.pack(fill=tk.BOTH, expand=True)
        self.current_text = '启动'

    def update_text(self, text):
        if self.current_text != text:
            timestamp = datetime.now().strftime("%H:%M:%S") #
            display_text = f"[{timestamp}] {text}" #
            self.label.config(text=display_text)
            self.root.update()
            self.current_text = text

class PicOverlay:
    def __init__(self, master):
        self.root = tk.Toplevel(master)
        self.root.attributes("-topmost", True)  # 置顶
        self.root.attributes("-transparentcolor", "black")
        self.root.overrideredirect(True)  # 无边框
        
        # 初始位置（右上角）
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry("300x200+{}+10".format(self.screen_width-310))
        
        init_img = np.zeros((200,300,4), dtype=np.uint8)
        img_pil = Image.fromarray(init_img)
        img_tk = ImageTk.PhotoImage(image=img_pil)

        self.label = tk.Label(self.root, image=img_tk, bg="black")
        self.label.pack()
        
    def update_overlay(self, overlay_image):
        # 将OpenCV图像转换为PIL格式
        overlay_image = cv2.cvtColor(overlay_image, cv2.COLOR_BGRA2RGBA)
        img_pil = Image.fromarray(overlay_image)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        
        self.label.configure(image=img_tk)
        self.label.image = img_tk  # 保持引用
        
        h, w = overlay_image.shape[:2]
        self.root.geometry(f"{w}x{h}+0+0")
        self.root.update()

    def hide_overlay(self): # Add this method
        init_img = np.zeros((1, 1, 4), dtype=np.uint8) # Create a 1x1 black image
        img_pil = Image.fromarray(init_img)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        self.label.configure(image=img_tk)
        self.label.image = img_tk
        self.root.geometry("1x1+0+0") # Make the window very small
        self.root.update()

def find_pic(image, pic, picrange, log_overlay, debug=False, pic_overlay=None):
    x1, y1, x2, y2 = picrange
    image_clip = image[y1:y2, x1:x2]
    template = cv2.imread(pic, cv2.IMREAD_UNCHANGED)

    value, loc_clip = match_pic(image_clip, template)
    loc = (loc_clip[0]+x1, loc_clip[1]+y1)

    res = (value < 0.015)

    if res:
        logging.info(f"{pic} {loc} {value}")
        log_overlay.update_text(f"{pic} {loc} {value:.3f}")
        if debug:
            h, w = template.shape[:2]
            image_overlay = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)
            draw_rect(image_overlay, value, loc, w, h, pic)
            pic_overlay.update_overlay(image_overlay)
    else:
        if debug:
            pic_overlay.hide_overlay()

    return res, loc

def match_pic(image, template):

    alpha = template[:,:,3]
    grey = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(image, grey, cv2.TM_SQDIFF_NORMED, mask=alpha)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    val = min_val
    loc = min_loc

    return val, loc

def draw_rect(image_overlay, val, loc, w, h, pic):
    cv2.rectangle(image_overlay, loc, (loc[0] + w, loc[1] + h), (0, 0, 255, 180), 2)
    #cv2.circle(image_overlay, (center_x, center_y), 5, (0, 255, 0, 200), -1)
    cv2.putText(image_overlay, f"{pic} {val:.3f}", (loc[0], loc[1] - 10), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(image_overlay, f"{loc}", (loc[0], loc[1] + h + 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255, 255), 1, cv2.LINE_AA)

def capture(hwnd: wintypes.HWND):
    
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
    
    image = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
    image_g = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)

    return image_g

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
