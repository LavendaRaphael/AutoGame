from winlib import get_window_title, is_key_pressed, skipping_cv
import time

def Nikky(hwnd, log_overlay, pic_overlay):
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
                    'pic':'InfinityNikky/dialog_0_0_450_136.png', 
                    "picxy": (0,0), 'picwh': (450,136), 
                    'actions': [
                        {'press':'F'}
                    ]
                }
            ]
            skipping_cv(log_overlay, pic_overlay, hwnd, pic_list)
        time.sleep(0.2)

def fishing(overlay):
    txt = "钓鱼模式, 按 A 拉线"
    overlay.update_text(txt)
    time.sleep(1)
    while True:
        if is_key_pressed("A"):
            overlay.update_text("拉线中 F 退出")
            while not is_key_pressed("F"):
                press('MOUSERIGHT')
                time.sleep(0.1)
            overlay.update_text(txt)
        elif is_key_pressed("]"):
            break
        time.sleep(0.1)
        