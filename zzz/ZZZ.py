from winlib import get_window_title, is_key_pressed, skipping, capture_mode
import time

def juqing(hwnd, log_overlay, pic_overlay):
    mode = log_overlay.mode
    log_overlay.update(mode = "剧情模式 退出 ]")
    pic_list = [
        {
            'pic':'ZZZ/pic/dialog_2140_1130_2220_1230_1.png', 
            "picxy": (2140,1130), 'picwh': (80 ,100), 
            'actions': [
                {'click': ('VK_LBUTTON', (100,50))}
            ],
        },
        {
            'pic':'ZZZ/pic/dialog_2140_1130_2220_1230_1.png', 
            "picxy": (0,0), 'picwh': (2880,1800), 
            'actions': [
                {'click': ('VK_LBUTTON', (100,50))}
            ],
        },
        {
            'pic':'ZZZ/pic/dialog_2140_1130_2220_1230.png'  , 
            "picxy": (2140,1130), 'picwh': (80 ,100), 
            'actions': [
                {'click': ('VK_LBUTTON', (100,50))}
            ],
        },{
            'pic':'ZZZ/pic/dialog_2140_1230_2220_1330.png'  , 
            "picxy": (2140,1248), 'picwh': (80 ,100), 
            'actions': [
                {'click': ('VK_LBUTTON', (100,50))}
            ],
        },{
            'pic':'ZZZ/pic/dialog_582_1404_860_1728.png'    , 
            "picxy": (582 ,1404), 'picwh': (278,324), 
            'actions': [
                {'press': 'VK_SPACE'}
            ],
        },{
            'pic':'ZZZ/pic/dialog_2140_1230_2220_1330.png'  , 
            "picxy": (2140,1230), 'picwh': (80 ,100), 
            'actions': [
                {'click': ('VK_LBUTTON', (100,50))}
            ],
        },{
            'pic':'ZZZ/pic/dialog_582_1404_860_1728.png'    , 
            "picxy": (582 ,1386), 'picwh': (278,324), 
            'actions': [
                {'press': 'VK_SPACE'}
            ],
        },{
            'pic':'ZZZ/pic/dialog_810_772_890_840.png'      , 
            "picxy": (810 ,772 ), 'picwh': (80 ,162), 
            'actions': [
                {'press': '1'}
            ],
        },{
            'pic':'ZZZ/pic/dialog_810_772_890_840.png'      , 
            "picxy": (810 ,678 ), 'picwh': (80 ,162), 
            'actions': [
                {'press': '1'}
            ],
        },{
            'pic':'ZZZ/pic/dialog_2472_258_2746_322.png'    , 
            "picxy": (2472,258 ), 'picwh': (274,64 ), 
            'actions': [
                {'press': 'VK_SPACE'}
            ],
        },{
            'pic': 'black',
            'method': 'color',
            'spec': 0.8,
            "picxy": (0,0), 'picwh': (2880, 1800 ), 
            'actions': [
                {'press': 'VK_SPACE'}
            ],
        },
    ]
    skipping(log_overlay, pic_overlay, hwnd, pic_list)
    log_overlay.update(mode = mode)
def ZZZ(hwnd, log_overlay, pic_overlay):
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
