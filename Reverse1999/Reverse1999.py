from winlib import get_window_title, is_key_pressed, skipping, capture_mode
import time

def juqing(hwnd, log_overlay, pic_overlay):
    mode = log_overlay.mode
    log_overlay.update(mode = "剧情模式 退出 ]")
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
    log_overlay.update(mode = mode)
def Reverse1999(hwnd, log_overlay, pic_overlay):
    log_overlay.update(mode = '剧情模式 ;')
    while True:
        hwnd_x, active_window = get_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            juqing(hwnd, log_overlay, pic_overlay)
        elif is_key_pressed("["):
            capture_mode(hwnd, log_overlay)
        time.sleep(0.2)
