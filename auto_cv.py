from winlib import get_foreground_window_title, is_key_pressed, LogOverlay, PicOverlay, skipping_cv
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

def ZZZ(hwnd, log_overlay, pic_overlay, active_window):
    txt = f"{active_window} ; 跳过"
    log_overlay.update_text(txt)
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            pic_dict = {
                'ZZZ/dialog_2073_1253_2128_1306.png': {"picrange": (2073,1153,2128,1324), 'key': '1'    ,"shift": (100,50)},
                'ZZZ/dialog_582_1404_860_1728.png'  : {"picrange": (582 ,1386,860 ,1728), 'key': 'SPACE',"shift": (100,0 )},
                'ZZZ/dialog_810_772_890_840.png'    : {"picrange": (810 ,772 ,890 ,934 ), 'key': '1'    ,"shift": (100,0 )},
                'ZZZ/dialog_2472_258_2746_322.png'  : {"picrange": (2472,258 ,2746,322 ), 'key': 'SPACE',"shift": (100,0 )},
            }
            skipping_cv(log_overlay, pic_overlay, hwnd, pic_dict)
            log_overlay.update_text(txt)
        time.sleep(0.2)

def Nikky(hwnd, log_overlay, pic_overlay, active_window):
    txt = f"{active_window} ; 跳过"
    log_overlay.update_text(txt)
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            pic_dict = {
                'InfinityNikky/dialog_0_0_450_136.png': {"picrange": (0,0,450,136), 'key': 'F', "shift": (100,0)},
            }
            skipping_cv(log_overlay, pic_overlay, hwnd, pic_dict)
            log_overlay.update_text(txt)
        time.sleep(0.2)

def StarRail(hwnd, log_overlay, pic_overlay, active_window):
    txt = f"{active_window} ; 跳过"
    log_overlay.update_text(txt)
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            pic_dict = {
                'StarRail/dialog_1885_1150_2020_1200.png': {"picrange": (1885,1150,2020,1322), 'key': 'MOUSELEFT', "shift": (200,0)},
                #'StarRail/dialog_1845_1027_1898_1077.png': {"picrange": (1845,1027,1898,1322), 'key': '1'    , "shift": (-100,0)},
                #'StarRail/dialog_1845_1149_1898_1200.png': {"picrange": (1845,1149,1898,1200), 'key': '1'    , "shift": (-100,0)},
                'StarRail/dialog_192_52_450_120.png'     : {"picrange": (192,   52, 450, 120), 'key': 'SPACE', "shift": (-100,0)},
            }
            skipping_cv(log_overlay, pic_overlay, hwnd, pic_dict)
            log_overlay.update_text(txt)
        time.sleep(0.2)

def Reverse1999(hwnd, log_overlay, pic_overlay, active_window):
    txt = f"{active_window} ; 跳过"
    log_overlay.update_text(txt)
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            pic_dict = {
                'Reverse1999/dialog_2314_162_2766_236.png': {"picrange": (2314,162,2766,236), 'key': 'SPACE', "shift": (-100,0)},
            }
            skipping_cv(log_overlay, pic_overlay, hwnd, pic_dict)
            log_overlay.update_text(txt)
        time.sleep(0.2)
    
def game_script_thread(log_overlay, pic_overlay):
    while True:
        hwnd, active_window = get_foreground_window_title()
        if active_window == "绝区零":
            ZZZ(hwnd, log_overlay, pic_overlay, active_window)
        elif active_window == "无限暖暖  ":
            Nikky(hwnd, log_overlay, pic_overlay, active_window)
        elif active_window == "崩坏：星穹铁道":
            StarRail(hwnd, log_overlay, pic_overlay, active_window)
        elif active_window == "MuMu模拟器12":
            Reverse1999(hwnd, log_overlay, pic_overlay, active_window)
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
