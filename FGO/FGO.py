from winlib import get_window_title, is_key_pressed, skipping, capture_mode
import time
from ultralytics import YOLO

def get_picdict():
    model = YOLO("FGO/best.pt")
    pic_dict = {
        'quest': {
            'pic':'FGO/pic/quest_2060_510_260_25.png', 
            "picxy": (2060, 510), 'picwh': (  260, 59), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -10, 0))}
            ]
        },
        'map1': {
            'pic':'map1',
            'method': 'yolo', 
            'model': model, 
            "picxy": ( 150, 200), 'picwh': (2720,1200), 
            'spec': 0.9,
            'actions': [
                {'click': ('VK_LBUTTON', ( -10, 100))}
            ]
        },
        'skipyes': {
            'pic':'FGO/pic/skipyes_1800_1320_1970_1400.png', 
            "picxy": (1800, 1320), 'picwh': ( 170, 80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 100))},
            ]
        },
        'skip':
        {
            'pic':'FGO/pic/skip_2550_125_2880_250.png', 
            "picxy": (2550, 125), 'picwh': ( 330, 125), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 100))},
            ]
        },
        'dialog':{
            'pic':'FGO/pic/dialog_350_470_100_100.png'        , 
            "picxy": ( 350, 470), 'picwh': ( 100, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 200, 100))}
            ]
        },
        'friendselect': {
            'pic':'FGO/pic/firendselect_1690_340_100_100.png', 
            "picxy": (1690, 340), 'picwh': ( 100, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 200))}
            ]
        },
        'friendselect1': {
            'pic':'FGO/pic/firendselect_1690_340_100_100.png', 
            "picxy": (1690, 340), 'picwh': ( 100, 100), 
            'actions': [
                {'break': 1}
            ]
        },
        'teamclose': {
            'pic':'FGO/pic/teamclose_1330_1400_1400_1500.png' , 
            "picxy": (1330,1400), 'picwh': (  70, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 100))},
                {'sleep':0.5},
                {'click': ('VK_LBUTTON', (-660,200))}
            ]
        },
        'teamclose1': {
            'pic':'FGO/pic/teamclose_1330_1400_1400_1500.png' , 
            "picxy": (1330,1400), 'picwh': (  70, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 100))},
            ]
        },
        'teamauto': {
            'pic':'FGO/pic/teamauto_1900_1420_1970_1500.png'  , 
            "picxy": (1900,1420), 'picwh': (  70,  80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 100))}
            ]
        },
        'teamauto1': {
            'pic':'FGO/pic/teamauto_1870_1320_70_80.png'      , 
            "picxy": (1870,1320), 'picwh': (  70,  80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -10,  50))}
            ]
        },
        'teamok': {
            'pic':'FGO/pic/teamok_2580_1580_2650_1650.png'    , 
            "picxy": (2580,1580), 'picwh': (  70,  70), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 100))}
            ]
        },
        'teamend': {
            'pic':'FGO/pic/teamend_970_1580_100_100.png'      , 
            "picxy": ( 970,1580), 'picwh': ( 100, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', (1600, 100))}
            ]
        },
        'attack': {
            'pic':'FGO/pic/attack_2600_1580_2800_1680.png'    , 
            "picxy": (2600,1580), 'picwh': ( 200, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', (-200,-200))}
            ]
        },
        'attackback': {
            'pic':'FGO/pic/attackback_2650_1600_2800_1680.png', 
            "picxy": (2650,1600), 'picwh': ( 150,  80), 
            'actions': [
                {'click': ('VK_LBUTTON', (-700,-1100))},
                {'sleep':0.1}, {'click': ('VK_LBUTTON',(-1300,-1100))},
                {'sleep':0.1}, {'click': ('VK_LBUTTON',(-1900,-1100))},
                {'sleep':0.1}, {'click': ('VK_LBUTTON',( -100, -400))},
                {'sleep':0.1}, {'click': ('VK_LBUTTON',( -700, -400))},
                {'sleep':0.1}, {'click': ('VK_LBUTTON',(-1300, -400))},
                {'sleep':0.1}, {'click': ('VK_LBUTTON',(-1900, -400))},
                {'sleep':0.1}, {'click': ('VK_LBUTTON',(-2500, -400))}
            ]
        },
        'star': {
            'pic':'FGO/pic/star_2170_1630_100_80.png', 
            "picxy": (2170,1630), 'picwh': ( 100,  80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 300, -100))}
            ]
        },
        'award': {
            'pic':'FGO/pic/award_0_1600_100_100.png', 
            "picxy": ( 0, 1600), 'picwh': ( 100, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, -100))}
            ]
        },
        'notice': {
            'pic':'FGO/pic/notice_1820_1330_80_80.png', 
            "picxy": (1820,1330), 'picwh': (  80,  80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -10,  10))}
            ]
        },
        'friendapply': {
            'pic':'FGO/pic/friendapply_2600_280_2750_350.png', 
            "picxy": (2600,280), 'picwh': ( 150, 70), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -2000,  1250))}
            ]
        },
        'network': {
            'pic':'FGO/pic/network_1730_1330_80_80.png', 
            "picxy": (1730,1330), 'picwh': ( 80, 80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -10,  10))}
            ]
        },
        'start': {
            'pic':'FGO/pic/start_2010_1340_60_60.png', 
            "picxy": (2010, 1340), 'picwh': (  60, 60), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -10, 0))}
            ]
        },
        'info': {
            'pic':'FGO/pic/info_2690_670_80_60.png', 
            "picxy": (2690, 670), 'picwh': (  80, 60), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -500, -10))},
                {'sleep': 0.5}
            ]
        },
        'again': {
            'pic':'FGO/pic/again_1740_1370_1820_1450.png', 
            "picxy": (1740,1370), 'picwh': (  80,  80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -10, 100))}
            ]
        },
        'apple': {
            'pic':'FGO/pic/apple_1940_1500_50_50.png', 
            "picxy": (1940,1500), 'picwh': ( 50, 50), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 0,  -700))},
            ]
        },
        'apple1': {
            'pic':'FGO/pic/apple_1940_1500_50_50.png', 
            "picxy": (1940,1500), 'picwh': ( 50, 50), 
            'actions': [
                {'break': 1},
            ]
        },
        'appleyes': {
            'pic':'FGO/pic/appleyes_1830_1330_80_80.png', 
            "picxy": (1830,1330), 'picwh': ( 80, 80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -10,  10))}
            ]
        },
    }
    return pic_dict

def rush(hwnd, log_overlay, pic_overlay):
    
    title = log_overlay.title
    log_overlay.update_title("刷本")

    pic_dict = get_picdict()
    pic_list1 = [
        pic_dict['apple'],
        pic_dict['appleyes'],
        pic_dict['start'],
        pic_dict['friendselect1'],
    ]
    pic_list2 = [
        pic_dict['start'],
        pic_dict['apple1'],
        pic_dict['info'],
        pic_dict['friendselect'],
        pic_dict['teamclose1'],
        pic_dict['teamend'],
        pic_dict['attack'],
        pic_dict['attackback'],
        pic_dict['star'],
        pic_dict['award'],
        pic_dict['friendapply'],
        pic_dict['again'],
        pic_dict['network'],
    ]
    apple = 5
    for i in range(apple):
        log_overlay.update_title(f"刷本 apple {i}/{apple}")
        stop = skipping(log_overlay, pic_overlay, hwnd, pic_list1)
        if stop:
            break
        stop = skipping(log_overlay, pic_overlay, hwnd, pic_list2)
        if stop:
            break

    log_overlay.update_title(title)

def mainquest(hwnd, log_overlay, pic_overlay):

    title = log_overlay.title
    log_overlay.update_title("主线")
    pic_dict = get_picdict()
    pic_list = [
        pic_dict['quest'],
        pic_dict['map1'],
        pic_dict['skipyes'],
        pic_dict['skip'],
        pic_dict['dialog'],
        pic_dict['friendselect'],
        pic_dict['teamclose'],
        pic_dict['teamauto'],
        pic_dict['teamauto1'],
        pic_dict['teamok'],
        pic_dict['teamend'],
        pic_dict['attack'],
        pic_dict['attackback'],
        pic_dict['star'],
        pic_dict['award'],
        pic_dict['notice'],
        pic_dict['friendapply'],
        pic_dict['network'],
    ]
    skipping(log_overlay, pic_overlay, hwnd, pic_list)
    log_overlay.update_title(title)

def FGO(hwnd, log_overlay, pic_overlay):
    title = f"FGO ; 主线 , 刷本"
    log_overlay.update_title(title)
    while True:
        hwnd_x, _ = get_window_title()
        if hwnd_x != hwnd:
            break
        elif is_key_pressed(";"):
            mainquest(hwnd, log_overlay, pic_overlay)
        elif is_key_pressed(","):
            rush(hwnd, log_overlay, pic_overlay)
        elif is_key_pressed("["):
            capture_mode(hwnd, log_overlay)
        time.sleep(0.2)
