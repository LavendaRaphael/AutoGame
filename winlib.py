import ctypes
import time
import tkinter as tk
from ctypes import windll,wintypes,create_unicode_buffer,byref, c_ubyte
import numpy as np
import cv2
from PIL import Image, ImageTk
import logging
from datetime import datetime

def capture_mode(hwnd, log_overlay):
    _, active_window = get_window_title(hwnd)
    title = log_overlay.title
    log_overlay.update_title(f"{active_window} 截图模式 ; 截图 ] 退出")
    while True:
        if is_key_pressed(";"):
            image = capture(hwnd)
            pic = f"cap/{time.strftime('%Y%m%d_%H%M%S')}.png"
            cv2.imwrite(pic, image)
            log_overlay.update_text(pic)
        elif is_key_pressed("]"):
            log_overlay.update_title(title)
            break

def click_piclist(image, pic_list, log_overlay, pic_overlay):
        for prop in pic_list:
            pic = prop['pic']
            key = prop['key']
            shift = prop['shift']
            picxy = prop['picxy']
            picwh = prop['picwh']
            picrange = (picxy[0], picxy[1], picxy[0]+picwh[0], picxy[1]+picwh[1])
            tof, loc = find_pic(image, pic, picrange, log_overlay, pic_overlay=pic_overlay)
            if tof:
                for (x,y) in shift:
                    press(key, (loc[0]+x, loc[1]+y))
                    time.sleep(0.1)
                break
        time.sleep(0.2)
        if not tof:
            pic_overlay.hide_overlay()

def skipping_cv(log_overlay, pic_overlay, hwnd, pic_list):
    _, active_window = get_window_title(hwnd)
    title = log_overlay.title
    log_overlay.update_title(f"{active_window} 跳过模式 ] 退出")
    time.sleep(1)
    while True:
        if is_key_pressed("]"):
            pic_overlay.hide_overlay()
            log_overlay.update_title(title)
            break
        image = capture(hwnd)
        for prop in pic_list:
            tof, loc = find_pic(prop, image, log_overlay, pic_overlay=pic_overlay)
            if tof:
                actions = prop['actions']
                for action in actions:
                    for act, value in action.items():
                        if act == 'sleep':
                            time.sleep(value)
                        else:
                            press(act, (loc[0]+value[0], loc[1]+value[1]))
                break
        time.sleep(0.2)
        if not tof:
            pic_overlay.hide_overlay()

def find_pic(prop, image, log_overlay, pic_overlay):
    picxy = prop['picxy']
    picwh = prop['picwh']
    picrange = (picxy[0], picxy[1], picxy[0]+picwh[0], picxy[1]+picwh[1])
    x1, y1, x2, y2 = picrange
    image_clip = image[y1:y2, x1:x2]
    method = prop.get('method', 'cv2')
    pic = prop['pic']
    if method == 'cv2':
        template = cv2.imread(pic, cv2.IMREAD_UNCHANGED)
        conf, loc_clip, w, h = match_pic(image_clip, template)
    elif method == 'yolo':
        model = prop['model']
        conf, loc_clip, w, h = match_pic_yolo(image_clip, model)
    else:
        raise
        
    loc = (loc_clip[0]+x1, loc_clip[1]+y1)

    spec = prop.get('spec', 0.985)
    res = (conf >= spec)
    if res:
        print(pic, loc, w, h, conf)
        logging.info(f"{pic} {loc} {conf}")
        log_overlay.update_text(f"{pic} {loc} {conf:.3f}")
        draw_rect(pic_overlay, loc, w, h, f"{pic} {conf:.3f}")

    return res, loc

def match_pic_yolo(image, model):
    image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    results = model.predict(image_bgr, conf=0.5)
    if len(results[0].boxes)>0:
        box = results[0].boxes[0]
        x1, y1, x2, y2 = box.xyxy.tolist()[0]
        loc = (int(x1), int(y1))
        w = int(x2 - x1)
        h = int(y2 - y1)
        conf = box.conf.item()
    else:
        conf = 0
        loc = (0,0)
        w = 0
        h = 0
    return conf, loc, w, h

def match_pic(image, template):

    alpha = template[:,:,3]
    grey = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(image, grey, cv2.TM_SQDIFF_NORMED, mask=alpha)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    val = min_val
    loc = min_loc
    conf = 1-val
    h, w = template.shape[:2]

    return conf, loc, w, h

def draw_rect(pic_overlay, loc, w, h, txt):
    image_overlay = np.zeros((pic_overlay.screen_height, pic_overlay.screen_width, 4), dtype=np.uint8)
    cv2.rectangle(image_overlay, loc, (loc[0] + w, loc[1] + h), (0, 0, 255, 180), 2)
    cv2.putText(image_overlay, txt, (loc[0], loc[1] - 10), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(image_overlay, f"{loc}", (loc[0], loc[1] + h + 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255, 255), 1, cv2.LINE_AA)
    pic_overlay.update_overlay(image_overlay)

class LogOverlay:
    def __init__(self, master):
        self.root = tk.Toplevel(master)
        self.root.title("Overlay")
        self.root.attributes("-topmost", True)  # 确保窗口始终在最前面
        self.root.attributes("-transparentcolor", "black")  # 设置透明色为黑色
        self.root.overrideredirect(True) # 无边框

        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.geometry(f"{screen_width}x100+0+{screen_height-100}")

        self.label = tk.Label(self.root, text="", font=("SimHei", 12, "bold"), fg="white", bg="black", anchor="w", justify='left')
        self.label.pack(fill=tk.BOTH, expand=True)

        self.title = 'AutoGame'
        self.timestamp = datetime.now().strftime("%H:%M:%S")
        self.text = '启动'
        self.update()

    def update_title(self, title):
        self.title = title
        self.update()

    def update_text(self, text):
        if self.text != text:
            self.text = text
            self.timestamp = datetime.now().strftime("%H:%M:%S")
            self.update()

    def update(self):
        display_text = f"{self.title}\n{self.timestamp} {self.text}"
        self.label.config(text=display_text)
        self.root.update()


class PicOverlay:
    def __init__(self, master):
        self.root = tk.Toplevel(master)
        self.root.attributes("-topmost", True)
        self.root.attributes("-transparentcolor", "black")
        self.root.overrideredirect(True)
        
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.screen_width}x{self.screen_height}+0+0")
        
        init_img = np.zeros((self.screen_height,self.screen_width,4), dtype=np.uint8)
        img_pil = Image.fromarray(init_img)
        self.init_img = ImageTk.PhotoImage(image=img_pil)

        self.label = tk.Label(self.root, image=self.init_img, bg="black")
        self.label.pack()
        
    def update_overlay(self, overlay_image):
        overlay_image = cv2.cvtColor(overlay_image, cv2.COLOR_BGRA2RGBA)
        img_pil = Image.fromarray(overlay_image)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        
        self.label.configure(image=img_tk)
        self.label.image = img_tk
        
        h, w = overlay_image.shape[:2]
        self.root.update()

    def hide_overlay(self):
        self.label.configure(image=self.init_img)
        self.label.image = self.init_img
        self.root.update()

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
        "2": 0x32,
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

def get_window_title(hwnd=None):
    if hwnd is None:
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
