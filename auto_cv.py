from winlib import get_window_title, LogOverlay, PicOverlay
import time
from ctypes import windll
import threading
import sys
import tkinter as tk
import logging
from InfinityNikky.InfinityNikky import Nikky
from ZZZ.ZZZ import ZZZ
from StarRail.StarRail import StarRail
from Reverse1999.Reverse1999 import Reverse1999

# 配置日志记录
logging.basicConfig(
    filename='debug.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

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
