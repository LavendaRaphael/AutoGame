import cv2
from winlib import get_foreground_window_title, is_key_pressed, capture, LogOverlay
import time
import sys
from ctypes import windll
import tkinter as tk
import logging
import cv2

logging.basicConfig(
    filename='debug.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

def main():

    windll.shcore.SetProcessDpiAwareness(2)
    if not windll.shell32.IsUserAnAdmin():
        windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        return
    
    root = tk.Tk()
    root.withdraw()
    
    log_overlay = LogOverlay(root)
    while True:
        hwnd, active_window = get_foreground_window_title()
        if is_key_pressed(";"):
            image = capture(hwnd)
            pic = f"cap/{time.strftime('%Y%m%d_%H%M%S')}.png"
            cv2.imwrite(pic, image)
            log_overlay.update_text(pic)
            logging.info(f"{active_window} {pic}")
        time.sleep(1)

if __name__ == "__main__":

    main()