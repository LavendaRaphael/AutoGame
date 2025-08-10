from winlib import get_window_title, is_key_pressed, skipping_cv
import time

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
                {'pic':'Reverse1999/dialog_2314_162_2766_236.png', "picxy": (2314,162), 'picwh': (452,74), 'key': 'SPACE', "shift": (-100,0)},
            ]
            skipping_cv(log_overlay, pic_overlay, hwnd, pic_list)
        time.sleep(0.2)
