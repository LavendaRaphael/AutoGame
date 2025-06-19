from winlib import get_foreground_window_title, is_key_pressed, press, capture, find_pic, LogOverlay, PicOverlay
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
def skipping(log_overlay, pic_overlay, hwnd):
    log_overlay.update_text("跳过模式 ] 退出")
    time.sleep(1)
    pic_dict = {
        'InfinityNikky/dialog_0_0_450_136.png': {"picrange": (0,0,450,136), "shift": (100,0)},
    }
    while True:
        if is_key_pressed("]"):
            break
        image = capture(hwnd)
        for pic, prop in pic_dict.items():
            picrange = prop['picrange']
            shift = prop['shift']
            tof, loc = find_pic(image, pic, picrange, log_overlay, debug=False, pic_overlay=pic_overlay)
            if tof:
                press('F')
                break
        time.sleep(0.2)

def mihoyo(hwnd, log_overlay, pic_overlay, active_window):
    txt = f"{active_window} ; 跳过"
    log_overlay.update_text(txt)
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            skipping(log_overlay, pic_overlay, hwnd)
            log_overlay.update_text(txt)
        time.sleep(0.2)

def game_script_thread(log_overlay, pic_overlay):
    while True:
        hwnd, active_window = get_foreground_window_title()
        if active_window in ["无限暖暖  "]:
        #if True:
            mihoyo(hwnd, log_overlay, pic_overlay, active_window)
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
