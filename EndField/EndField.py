from winlib import get_window_title, is_key_pressed, skipping, capture_mode
import time
from ultralytics import YOLO

def juqing(hwnd, log_overlay, pic_overlay):
    mode = log_overlay.mode
    log_overlay.update(mode = "剧情模式 退出 ]")
    model = YOLO("EndField/best.pt")
    pic_list = [
        {
            'pic':'dialogesc',
            'method': 'yolo', 
            'model': model, 
            "picxy": ( 0, 0), 'picwh': (2880,1800), 
            'spec': 0.4,
            'actions': [
                {'click': ('VK_LBUTTON', ( 10, 10))}
            ]
        },
        {
            'pic':'EndField/pic/queren1_1760_1140_80_50.png', 
            "picxy": (1760,1140), 'picwh': (80 ,50), 
            'actions': [
                {'click': ('VK_LBUTTON', (-10,0))}
            ],
        },
        {
            'pic':'EndField/pic/queren2_1746_1110_80_50.png', 
            "picxy": (1746,1110), 'picwh': (80 ,50), 
            'actions': [
                {'click': ('VK_LBUTTON', (-10,0))}
            ],
        },
    ]
    skipping(log_overlay, pic_overlay, hwnd, pic_list)
    log_overlay.update(mode = mode)

def EndField(hwnd, log_overlay, pic_overlay):
    log_overlay.update(mode = "模式 剧情 ;")
    while True:
        hwnd_x, _ = get_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            juqing(hwnd, log_overlay, pic_overlay)
        elif is_key_pressed("["):
            capture_mode(hwnd, log_overlay)
        time.sleep(0.2)
