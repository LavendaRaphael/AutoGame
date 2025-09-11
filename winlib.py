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

def skipping(log_overlay, pic_overlay, hwnd, pic_list):

    title = log_overlay.title
    log_overlay.update_title(f"{title} ] 退出")
    time.sleep(1)
    while True:
        if is_key_pressed("]"):
            pic_overlay.hide_overlay()
            log_overlay.update_title(title)
            return True
        image = capture(hwnd)
        for prop in pic_list:
            tof, loc = find_pic(prop, image, log_overlay, pic_overlay=pic_overlay)
            if tof:
                actions = prop['actions']
                for action in actions:
                    for act, value in action.items():
                        if act == 'sleep':
                            time.sleep(value)
                        elif act == 'click':
                            key = value[0]
                            pos = (loc[0]+value[1][0], loc[1]+value[1][1])
                            click_mouse(key, pos)
                        elif act == 'press':
                            press_key(value)
                        elif act == 'break':
                            pic_overlay.hide_overlay()
                            log_overlay.update_title(title)
                            return False
                        else:
                            raise
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
    spec = prop.get('spec', 0.985)
    if method == 'cv2':
        template = cv2.imread(pic, cv2.IMREAD_UNCHANGED)
        conf, loc_clip, w, h = match_pic(image_clip, template)
    elif method == 'yolo':
        model = prop['model']
        conf, loc_clip, w, h = match_pic_yolo(image_clip, model, spec)
    else:
        raise
        
    loc = (loc_clip[0]+x1, loc_clip[1]+y1)

    res = (conf >= spec)
    if res:
        logging.info(f"{pic} {loc} {conf}")
        log_overlay.update_text(f"{pic} {loc} {conf:.3f}")
        draw_rect(pic_overlay, loc, w, h, f"{pic} {conf:.3f}")

    return res, loc

def match_pic_yolo(image, model, spec=0.5):
    image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    results = model.predict(image_bgr, conf=spec)
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

def press_key(keyname):
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
        "VK_LBUTTON": (MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP),
        "VK_RBUTTON": (MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP),
        "VK_MBUTTON": (MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP),
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

# 按键代码定义
def vk_codes(name):
    codes = {
        'VK_LBUTTON' : 0x01,
        'VK_RBUTTON' : 0x02,
        'VK_CANCEL'  : 0x03,
        'VK_MBUTTON' : 0x04,
        'VK_XBUTTON1': 0x05,
        'VK_XBUTTON2': 0x06,
        'VK_BACK': 0x08,
        'VK_TAB': 0x09,
        'VK_CLEAR': 0x0C,
        'VK_RETURN': 0x0D,
        'VK_SHIFT': 0x10,
        'VK_CONTROL': 0x11,
        'VK_MENU': 0x12,
        'VK_PAUSE': 0x13,
        'VK_CAPITAL': 0x14,
        'VK_KANA': 0x15,
        'VK_HANGUL': 0x15,
        'VK_IME_ON': 0x16,
        'VK_JUNJA': 0x17,
        'VK_FINAL': 0x18,
        'VK_HANJA': 0x19,
        'VK_KANJI': 0x19,
        'VK_IME_OFF': 0x1A,
        'VK_ESCAPE': 0x1B,
        'VK_CONVERT': 0x1C,
        'VK_NONCONVERT': 0x1D,
        'VK_ACCEPT': 0x1E,
        'VK_MODECHANGE': 0x1F,
        'VK_SPACE': 0x20,
        'VK_PRIOR': 0x21,
        'VK_NEXT': 0x22,
        'VK_END': 0x23,
        'VK_HOME': 0x24,
        'VK_LEFT': 0x25,
        'VK_UP': 0x26,
        'VK_RIGHT': 0x27,
        'VK_DOWN': 0x28,
        'VK_SELECT': 0x29,
        'VK_PRINT': 0x2A,
        'VK_EXECUTE': 0x2B,
        'VK_SNAPSHOT': 0x2C,
        'VK_INSERT': 0x2D,
        'VK_DELETE': 0x2E,
        'VK_HELP': 0x2F,
        '0': 0x30,
        '1': 0x31,
        '2': 0x32,
        '3': 0x33,
        '4': 0x34,
        '5': 0x35,
        '6': 0x36,
        '7': 0x37,
        '8': 0x38,
        '9': 0x39,
        'A': 0x41,
        'B': 0x42,
        'C': 0x43,
        'D': 0x44,
        'E': 0x45,
        'F': 0x46,
        'G': 0x47,
        'H': 0x48,
        'I': 0x49,
        'J': 0x4A,
        'K': 0x4B,
        'L': 0x4C,
        'M': 0x4D,
        'N': 0x4E,
        'O': 0x4F,
        'P': 0x50,
        'Q': 0x51,
        'R': 0x52,
        'S': 0x53,
        'T': 0x54,
        'U': 0x55,
        'V': 0x56,
        'W': 0x57,
        'X': 0x58,
        'Y': 0x59,
        'Z': 0x5A,
        'VK_LWIN': 0x5B,
        'VK_RWIN': 0x5C,
        'VK_APPS': 0x5D,
        'VK_SLEEP': 0x5F,
        'VK_NUMPAD0': 0x60,
        'VK_NUMPAD1': 0x61,
        'VK_NUMPAD2': 0x62,
        'VK_NUMPAD3': 0x63,
        'VK_NUMPAD4': 0x64,
        'VK_NUMPAD5': 0x65,
        'VK_NUMPAD6': 0x66,
        'VK_NUMPAD7': 0x67,
        'VK_NUMPAD8': 0x68,
        'VK_NUMPAD9': 0x69,
        'VK_MULTIPLY': 0x6A,
        'VK_ADD': 0x6B,
        'VK_SEPARATOR': 0x6C,
        'VK_SUBTRACT': 0x6D,
        'VK_DECIMAL': 0x6E,
        'VK_DIVIDE': 0x6F,
        'VK_F1': 0x70,
        'VK_F2': 0x71,
        'VK_F3': 0x72,
        'VK_F4': 0x73,
        'VK_F5': 0x74,
        'VK_F6': 0x75,
        'VK_F7': 0x76,
        'VK_F8': 0x77,
        'VK_F9': 0x78,
        'VK_F10': 0x79,
        'VK_F11': 0x7A,
        'VK_F12': 0x7B,
        'VK_F13': 0x7C,
        'VK_F14': 0x7D,
        'VK_F15': 0x7E,
        'VK_F16': 0x7F,
        'VK_F17': 0x80,
        'VK_F18': 0x81,
        'VK_F19': 0x82,
        'VK_F20': 0x83,
        'VK_F21': 0x84,
        'VK_F22': 0x85,
        'VK_F23': 0x86,
        'VK_F24': 0x87,
        'VK_NUMLOCK': 0x90,
        'VK_SCROLL': 0x91,
        'VK_LSHIFT': 0xA0,
        'VK_RSHIFT': 0xA1,
        'VK_LCONTROL': 0xA2,
        'VK_RCONTROL': 0xA3,
        'VK_LMENU': 0xA4,
        'VK_RMENU': 0xA5,
        'VK_BROWSER_BACK': 0xA6,
        'VK_BROWSER_FORWARD': 0xA7,
        'VK_BROWSER_REFRESH': 0xA8,
        'VK_BROWSER_STOP': 0xA9,
        'VK_BROWSER_SEARCH': 0xAA,
        'VK_BROWSER_FAVORITES': 0xAB,
        'VK_BROWSER_HOME': 0xAC,
        'VK_VOLUME_MUTE': 0xAD,
        'VK_VOLUME_DOWN': 0xAE,
        'VK_VOLUME_UP': 0xAF,
        'VK_MEDIA_NEXT_TRACK': 0xB0,
        'VK_MEDIA_PREV_TRACK': 0xB1,
        'VK_MEDIA_STOP': 0xB2,
        'VK_MEDIA_PLAY_PAUSE': 0xB3,
        'VK_LAUNCH_MAIL': 0xB4,
        'VK_LAUNCH_MEDIA_SELECT': 0xB5,
        'VK_LAUNCH_APP1': 0xB6,
        'VK_LAUNCH_APP2': 0xB7,
        'VK_OEM_1': 0xBA, ';': 0xBA,
        'VK_OEM_PLUS': 0xBB,
        'VK_OEM_COMMA': 0xBC, ',': 0xBC,
        'VK_OEM_MINUS': 0xBD,
        'VK_OEM_PERIOD': 0xBE, '.': 0xBE,
        'VK_OEM_2': 0xBF,
        'VK_OEM_3': 0xC0,
        'VK_OEM_4': 0xDB, '[': 0xDB,
        'VK_OEM_5': 0xDC,
        'VK_OEM_6': 0xDD, ']': 0xDD,
        'VK_OEM_7': 0xDE,
        'VK_OEM_8': 0xDF,
        'VK_OEM_102': 0xE2,
        'VK_PROCESSKEY': 0xE5,
        'VK_PACKET': 0xE7,
        'VK_ATTN': 0xF6,
        'VK_CRSEL': 0xF7,
        'VK_EXSEL': 0xF8,
        'VK_EREOF': 0xF9,
        'VK_PLAY': 0xFA,
        'VK_ZOOM': 0xFB,
        'VK_NONAME': 0xFC,
        'VK_PA1': 0xFD,
        'VK_OEM_CLEAR': 0xFE,
    }
    return codes[name]
