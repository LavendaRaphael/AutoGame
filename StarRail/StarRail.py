from winlib import capture_mode, get_window_title, is_key_pressed, skipping
import time

def juqing(hwnd, log_overlay, pic_overlay):
    mode = log_overlay.mode
    log_overlay.update(mode = "剧情模式 退出 ]")
    pic_list = [
        {
            'pic':'StarRail/pic/dialog_1885_1150_2020_1200.png', 
            "picxy": (1885,1150),'picwh':(135,172), 
            'actions': [
                {'click': ('VK_LBUTTON', (200,0))}
            ]
        },{
            'pic':'StarRail/pic/dialog_192_52_450_120.png', 
            "picxy": (192,   52),'picwh':(258,68), 
            'actions': [
                {'press': 'VK_SPACE'},
            ]
        },{
            'pic':'StarRail/pic/queren_1680_1072_50_50.png', 
            "picxy": (1680,1072),'picwh':(50,50), 
            'actions': [
                {'click': ('VK_LBUTTON', (200,0))}
            ]
        }
    ]
    skipping(log_overlay, pic_overlay, hwnd, pic_list)
    log_overlay.update(mode = mode)
def StarRail(hwnd, log_overlay, pic_overlay):
    log_overlay.update(mode = '剧情模式 ;')
    while True:
        hwnd_x, _ = get_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            juqing(hwnd, log_overlay, pic_overlay)
        elif is_key_pressed("["):
            capture_mode(hwnd, log_overlay)
        time.sleep(0.2)
