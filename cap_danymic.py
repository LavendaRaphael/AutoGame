import cv2
import numpy as np
from winlib import get_foreground_window_title, is_key_pressed, capture, LogOverlay
import time
import sys
from ctypes import windll
import tkinter as tk

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
            image_last = capture(hwnd)
            for i in range(10):
                image_now = capture(hwnd)
                diff = cv2.absdiff(image_last, image_now)
                _, image = cv2.threshold(diff, 2, 255, cv2.THRESH_BINARY)
                pic = f"cap/{time.strftime('%Y%m%d_%H%M%S')}_{i}.png"
                cv2.imwrite(pic, image)
                log_overlay.update_text(pic)
                image_last = image_now
                time.sleep(0.2)

if __name__ == "__main__":

    main()