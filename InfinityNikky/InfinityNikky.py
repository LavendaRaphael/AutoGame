from winlib import get_window_title, is_key_pressed, skipping, capture_mode
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
                    'pic':'InfinityNikky/pic/history_70_45_70_70.png', 
                    "picxy": (70,45), 'picwh': (70,70), 
                    'actions': [
                        {'press':'F'}
                    ]
                },
                {
                    'pic':'InfinityNikky/pic/F_2520_1690_40_40.png', 
                    "picxy": (2352,1720), 'picwh': (40,40), 
                    'actions': [
                        {'press':'F'}
                    ]
                },
                {
                    'pic':'InfinityNikky/pic/F_2520_1690_40_40.png', 
                    "picxy": (2568,1704), 'picwh': (40,40), 
                    'actions': [
                        {'press':'F'}
                    ]
                },
                {
                    'pic':'InfinityNikky/pic/F_2520_1690_40_40.png', 
                    "picxy": (2424,1720), 'picwh': (40,40), 
                    'actions': [
                        {'press':'F'}
                    ]
                },
                #{
                #    'pic':'InfinityNikky/pic/F_2520_1690_40_40.png', 
                #    "picxy": (2300,1690), 'picwh': (400,100), 
                #    'actions': [
                #        {'press':'F'}
                #    ]
                #}
            ]
            skipping(log_overlay, pic_overlay, hwnd, pic_list)
        elif is_key_pressed("["):
            capture_mode(hwnd, log_overlay)
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
        