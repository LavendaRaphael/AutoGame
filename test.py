from winlib import match_pic,is_key_pressed,get_foreground_window_title,capture
import cv2
from ctypes import windll

#windll.shcore.SetProcessDpiAwareness(2)
windll.user32.SetProcessDPIAware()

while True:
    if is_key_pressed(";"):
        #pic1 = cv2.imread('cap/test1.png', cv2.IMREAD_UNCHANGED)
        hwnd, active_window = get_foreground_window_title()
        image = capture(hwnd)
        val, loc, overlay = match_pic(image, 'zzz/dialog_1.png', debug='image')
        cv2.imwrite(f"cap/test.png", image)
        cv2.imshow('overlay', overlay)
        cv2.waitKey(0)