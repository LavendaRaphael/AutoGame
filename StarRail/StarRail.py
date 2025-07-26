from winlib import get_window_title, is_key_pressed, skipping_cv
import time

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
