from winlib import get_window_title, is_key_pressed, LogOverlay, PicOverlay, skipping_cv, capture_mode
import time
from ctypes import windll
import threading
import sys
import tkinter as tk
import logging

# 配置日志记录
logging.basicConfig(
    filename='debug.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def ZZZ(hwnd, log_overlay, pic_overlay):
    _, active_window = get_window_title(hwnd)
    title = f"{active_window} ; 跳过"
    log_overlay.update_title(title)
    while True:
        hwnd_x, _ = get_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            pic_list = [
                {'pic':'ZZZ/dialog_2140_1130_2220_1230_1.png', "picxy": (2140,1130), 'picwh': (80 ,100), 'key': 'MOUSELEFT',"shift": (100,50)},
                {'pic':'ZZZ/dialog_2140_1130_2220_1230.png'  , "picxy": (2140,1130), 'picwh': (80 ,100), 'key': 'MOUSELEFT',"shift": (100,50)},
                {'pic':'ZZZ/dialog_2140_1230_2220_1330.png'  , "picxy": (2140,1248), 'picwh': (80 ,100), 'key': 'MOUSELEFT',"shift": (100,50)},
                {'pic':'ZZZ/dialog_582_1404_860_1728.png'    , "picxy": (582 ,1404), 'picwh': (278,324), 'key': 'SPACE'    ,"shift": (100,0)},
                {'pic':'ZZZ/dialog_2140_1230_2220_1330.png'  , "picxy": (2140,1230), 'picwh': (80 ,100), 'key': 'MOUSELEFT',"shift": (100,50)},
                {'pic':'ZZZ/dialog_582_1404_860_1728.png'    , "picxy": (582 ,1386), 'picwh': (278,324), 'key': 'SPACE'    ,"shift": (100,0)},
                {'pic':'ZZZ/dialog_810_772_890_840.png'      , "picxy": (810 ,772 ), 'picwh': (80 ,162), 'key': '1'        ,"shift": (100,0)},
                {'pic':'ZZZ/dialog_810_772_890_840.png'      , "picxy": (810 ,678 ), 'picwh': (80 ,162), 'key': '1'        ,"shift": (100,0)},
                {'pic':'ZZZ/dialog_2472_258_2746_322.png'    , "picxy": (2472,258 ), 'picwh': (274,64 ), 'key': 'SPACE'    ,"shift": (100,0)},
            ]
            skipping_cv(log_overlay, pic_overlay, hwnd, pic_list)
        elif is_key_pressed("["):
            capture_mode(hwnd, log_overlay)
        time.sleep(0.2)

def Nikky(hwnd, log_overlay, pic_overlay):
    _, active_window = get_window_title(hwnd)
    title = f"{active_window} ; 跳过"
    log_overlay.update_title(title)
    while True:
        hwnd_x, active_window = get_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            pic_list = [
                {'pic':'InfinityNikky/dialog_0_0_450_136.png', "picrange": (0,0,450,136), 'key': 'F', "shift": (100,0)},
            ]
            skipping_cv(log_overlay, pic_overlay, hwnd, pic_list)
        time.sleep(0.2)

def StarRail(hwnd, log_overlay, pic_overlay):
    _, active_window = get_window_title(hwnd)
    title = f"{active_window} ; 跳过"
    log_overlay.update_title(title)
    while True:
        hwnd_x, active_window = get_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            pic_list = [
                {'pic':'StarRail/dialog_1885_1150_2020_1200.png', "picrange": (1885,1150,2020,1322), 'key': 'MOUSELEFT', "shift": (200,0)},
                {'pic':'StarRail/dialog_192_52_450_120.png'     , "picrange": (192,   52, 450, 120), 'key': 'SPACE', "shift": (-100,0)},
            ]
            skipping_cv(log_overlay, pic_overlay, hwnd, pic_list)
        time.sleep(0.2)

def Reverse1999(hwnd, log_overlay, pic_overlay):
    _, active_window = get_window_title(hwnd)
    title = f"{active_window} ; 跳过"
    log_overlay.update_title(title)
    while True:
        hwnd_x, active_window = get_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            pic_list = [
                {'pic':'Reverse1999/dialog_2314_162_2766_236.png', "picrange": (2314,162,2766,236), 'key': 'SPACE', "shift": (-100,0)},
            ]
            skipping_cv(log_overlay, pic_overlay, hwnd, pic_list)
        time.sleep(0.2)
    
def game_script_thread(log_overlay, pic_overlay):
    while True:
        hwnd, active_window = get_window_title()
        if active_window == "绝区零":
            ZZZ(hwnd, log_overlay, pic_overlay)
        elif active_window == "无限暖暖  ":
            Nikky(hwnd, log_overlay, pic_overlay)
        elif active_window == "崩坏：星穹铁道":
            StarRail(hwnd, log_overlay, pic_overlay)
        elif active_window == "MuMu模拟器12":
            Reverse1999(hwnd, log_overlay, pic_overlay)
        else:
            log_overlay.update_text(f"当前窗口: {active_window}")
        time.sleep(1)

def main():
    
    windll.shcore.SetProcessDpiAwareness(2)
    if not windll.shell32.IsUserAnAdmin():
        windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        return
    
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    log_overlay = LogOverlay(root)
    pic_overlay = PicOverlay(root)
    
    script_thread = threading.Thread(target=game_script_thread,
                                    args=(log_overlay, pic_overlay), 
                                    daemon=True)
    script_thread.start()
    
    root.mainloop()

if __name__ == "__main__":
    main()
