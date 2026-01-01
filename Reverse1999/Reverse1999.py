from winlib import get_window_title, is_key_pressed, skipping, capture_mode
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
                {
                    'pic':'Reverse1999/pic/dialog_2314_162_2766_236.png', 
                    "picxy": (2314,162), 'picwh': (452,74), 
                    'actions': [
                        {'press': 'VK_SPACE'}
                    ]
                },
            ]
            skipping(log_overlay, pic_overlay, hwnd, pic_list)
        elif is_key_pressed("["):
            capture_mode(hwnd, log_overlay)
        time.sleep(0.2)
