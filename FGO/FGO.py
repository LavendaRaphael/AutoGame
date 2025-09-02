from winlib import get_window_title, is_key_pressed, skipping_cv, capture_mode, capture
import time
from ultralytics import YOLO

def grand(hwnd, log_overlay, pic_overlay):
    pic_list = [
        {
            'pic':'FGO/start_2010_1340_60_60.png', 
            "picxy": (2010, 1340), 'picwh': (  60, 60), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -10, 0))}
            ]
        },{
            'pic':'FGO/fuben_2690_670_80_60.png', 
            "picxy": (2690, 670), 'picwh': (  80, 60), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -500, -10))}
            ]
        },{
            'pic':'FGO/firendselect_1690_340_100_100.png', 
            "picxy": (1690, 340), 'picwh': ( 100, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 200))}
            ]
        },{
            'pic':'FGO/teamclose_1330_1400_1400_1500.png' , 
            "picxy": (1330,1400), 'picwh': (  70, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 100))},
            ]
        },{
            'pic':'FGO/teamend_970_1580_100_100.png'      , 
            "picxy": ( 970,1580), 'picwh': ( 100, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', (1600, 100))}
            ]
        },{
            'pic':'FGO/attack_2600_1580_2800_1680.png'    , 
            "picxy": (2600,1580), 'picwh': ( 200, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', (-200,-200))}
            ]
        },{
            'pic':'FGO/attackback_2650_1600_2800_1680.png', 
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
        },{
            'pic':'FGO/star_2170_1630_100_80.png', 
            "picxy": (2170,1630), 'picwh': ( 100,  80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 300, -100))}
            ]
        },{
            'pic':'FGO/award_0_1600_100_100.png', 
            "picxy": ( 0, 1600), 'picwh': ( 100, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, -100))}
            ]
        },{
            'pic':'FGO/again_1740_1370_1820_1450.png', 
            "picxy": (1740,1370), 'picwh': (  80,  80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -10, 100))}
            ]
        },{
            'pic':'FGO/friendapply_2600_280_2750_350.png', 
            "picxy": (2600,280), 'picwh': ( 150, 70), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -2000,  1250))}
            ]
        },{
            'pic':'FGO/apple_1940_1500_50_50.png', 
            "picxy": (1940,1500), 'picwh': ( 50, 50), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 0,  -700))}
            ]
        },{
        #    'pic':'FGO/appleyes_1830_1330_80_80.png', 
        #    "picxy": (1830,1330), 'picwh': ( 80, 80), 
        #    'actions': [
        #        {'click': ('VK_LBUTTON', ( -10,  10))}
        #    ]
        #},{
            'pic':'FGO/network_1730_1330_80_80.png', 
            "picxy": (1730,1330), 'picwh': ( 80, 80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -10,  10))}
            ]
        },
    ]
    skipping_cv(log_overlay, pic_overlay, hwnd, pic_list)

def mainquest(hwnd, log_overlay, pic_overlay):
    model = YOLO("FGO/best.pt")
    pic_list = [
        {
            'pic':'FGO/quest_2060_510_260_25.png', 
            "picxy": (2060, 510), 'picwh': (  260, 59), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -10, 0))}
            ]
        },{
            'pic':'map1',
            'method': 'yolo', 
            'model': model , 
            "picxy": ( 150, 200), 'picwh': (2720,1200), 
            'spec': 0.9,
            'actions': [
                {'click': ('VK_LBUTTON', ( -10, 100))}
            ]
        },{
            'pic':'FGO/skipyes_1800_1320_1970_1400.png', 
            "picxy": (1800, 1320), 'picwh': ( 170, 80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 100))},
            ]
        },{
            'pic':'FGO/skip_2550_125_2880_250.png', 
            "picxy": (2550, 125), 'picwh': ( 330, 125), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 100))},
            ]
        },{
            'pic':'FGO/dialog_350_470_100_100.png'        , 
            "picxy": ( 350, 470), 'picwh': ( 100, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 200, 100))}
            ]
        },{
            'pic':'FGO/firendselect_1690_340_100_100.png', 
            "picxy": (1690, 340), 'picwh': ( 100, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 200))}
            ]
        },{
            'pic':'FGO/teamclose_1330_1400_1400_1500.png' , 
            "picxy": (1330,1400), 'picwh': (  70, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 100))},
                {'sleep':0.5},
                {'click': ('VK_LBUTTON', (-660,200))}
            ]
        },{
            'pic':'FGO/teamauto_1900_1420_1970_1500.png'  , 
            "picxy": (1900,1420), 'picwh': (  70,  80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 100))}
            ]
        },{
            'pic':'FGO/teamauto_1870_1320_70_80.png'      , 
            "picxy": (1870,1320), 'picwh': (  70,  80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -10,  50))}
            ]
        },{
            'pic':'FGO/teamok_2580_1580_2650_1650.png'    , 
            "picxy": (2580,1580), 'picwh': (  70,  70), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, 100))}
            ]
        },{
            'pic':'FGO/teamend_970_1580_100_100.png'      , 
            "picxy": ( 970,1580), 'picwh': ( 100, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', (1600, 100))}
            ]
        },{
            'pic':'FGO/attack_2600_1580_2800_1680.png'    , 
            "picxy": (2600,1580), 'picwh': ( 200, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', (-200,-200))}
            ]
        },{
            'pic':'FGO/attackback_2650_1600_2800_1680.png', 
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
        },{
            'pic':'FGO/star_2170_1630_100_80.png', 
            "picxy": (2170,1630), 'picwh': ( 100,  80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 300, -100))}
            ]
        },{
            'pic':'FGO/award_0_1600_100_100.png', 
            "picxy": ( 0, 1600), 'picwh': ( 100, 100), 
            'actions': [
                {'click': ('VK_LBUTTON', ( 100, -100))}
            ]
        },{
            'pic':'FGO/notice_1820_1330_80_80.png', 
            "picxy": (1820,1330), 'picwh': (  80,  80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -10,  10))}
            ]
        },{
            'pic':'FGO/friendapply_2600_280_2750_350.png', 
            "picxy": (2600,280), 'picwh': ( 150, 70), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -2000,  1250))}
            ]
        },{
            'pic':'FGO/network_1730_1330_80_80.png', 
            "picxy": (1730,1330), 'picwh': ( 80, 80), 
            'actions': [
                {'click': ('VK_LBUTTON', ( -10,  10))}
            ]
        },
    ]
    skipping_cv(log_overlay, pic_overlay, hwnd, pic_list)

def FGO(hwnd, log_overlay, pic_overlay):
    _, active_window = get_window_title(hwnd)
    title = f"{active_window} ; 主线 , 冠位战"
    log_overlay.update_title(title)
    while True:
        hwnd_x, active_window = get_window_title()
        if hwnd_x != hwnd:
            break
        elif is_key_pressed(";"):
            mainquest(hwnd, log_overlay, pic_overlay)
        elif is_key_pressed(","):
            grand(hwnd, log_overlay, pic_overlay)
        elif is_key_pressed("["):
            capture_mode(hwnd, log_overlay)
        time.sleep(0.2)
