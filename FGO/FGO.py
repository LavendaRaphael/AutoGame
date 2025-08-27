from winlib import get_window_title, is_key_pressed, skipping_cv, capture_mode, capture
import time
from ultralytics import YOLO

def mainquest(hwnd, log_overlay, pic_overlay):
    model = YOLO("FGO/best.pt")
    pic_list = [
        {'pic':'FGO/mainquest_1770_450_1850_550.png'   , "picxy": (1770, 450), 'picwh': (  80, 100), 'actions': [{'MOUSELEFT': ( 100, 100)}]},
        {'pic':'map1','method': 'yolo', 'model': model , "picxy": (   0,   0), 'picwh': (2890,1725), 'actions': [{'MOUSELEFT': ( -10,  50)}], 'spec': 0.9},
        {'pic':'FGO/skip_2550_125_2880_250.png'        , "picxy": (2550, 125), 'picwh': ( 330, 125), 'actions': [{'MOUSELEFT': ( 100, 100)},{'sleep':0.5},{'MOUSELEFT':(-700,1225)}]},
        {'pic':'FGO/dialog_350_470_100_100.png'        , "picxy": ( 350, 470), 'picwh': ( 100, 100), 'actions': [{'MOUSELEFT': ( 200, 100)}]},
        {'pic':'FGO/friendselect_1680_340_1800_450.png', "picxy": (1680, 340), 'picwh': ( 120, 110), 'actions': [{'MOUSELEFT': ( 100, 200)}]},
        {'pic':'FGO/teamclose_1330_1400_1400_1500.png' , "picxy": (1330,1400), 'picwh': (  70, 100), 'actions': [{'MOUSELEFT': ( 100, 100)},{'sleep':0.5},{'MOUSELEFT':(-660,200)}]},
        {'pic':'FGO/teamauto_1900_1420_1970_1500.png'  , "picxy": (1900,1420), 'picwh': (  70,  80), 'actions': [{'MOUSELEFT': ( 100, 100)}]},
        {'pic':'FGO/teamauto_1870_1320_70_80.png'      , "picxy": (1870,1320), 'picwh': (  70,  80), 'actions': [{'MOUSELEFT': ( -10,  50)}]},
        {'pic':'FGO/teamok_2580_1580_2650_1650.png'    , "picxy": (2580,1580), 'picwh': (  70,  70), 'actions': [{'MOUSELEFT': ( 100, 100)}]},
        {'pic':'FGO/teamend_970_1580_100_100.png'      , "picxy": ( 970,1580), 'picwh': ( 100, 100), 'actions': [{'MOUSELEFT': (1600, 100)}]},
        {'pic':'FGO/attack_2600_1580_2800_1680.png'    , "picxy": (2600,1580), 'picwh': ( 200, 100), 'actions': [{'MOUSELEFT': (-200,-200)}]},
        {'pic':'FGO/attackback_2650_1600_2800_1680.png', "picxy": (2650,1600), 'picwh': ( 150,  80), 
            'actions': [
                {'MOUSELEFT': (-700,-1100)},
                {'MOUSELEFT': (-1300,-1100)},
                {'MOUSELEFT': (-1900,-1100)},
                {'MOUSELEFT': (-100,-400)},
                {'MOUSELEFT':(-700,-400)},
                {'MOUSELEFT':(-1300,-400)},
                {'MOUSELEFT':(-1900,-400)},
                {'MOUSELEFT':(-2500,-400)}
            ]},
        {'pic':'FGO/getzhanli_2400_1500_2550_1600.png' , "picxy": (2400,1500), 'picwh': ( 150, 100), 'actions': [{'MOUSELEFT': (-100, 100)}]},
        {'pic':'FGO/getjiban_180_480_260_550.png'      , "picxy": ( 180, 480), 'picwh': (  80,  70), 'actions': [{'MOUSELEFT': ( 100, 100)}]},
        {'pic':'FGO/getexp_1470_530_1550_600.png'      , "picxy": (1470, 530), 'picwh': (  80,  70), 'actions': [{'MOUSELEFT': ( 100, 100)}]},
        {'pic':'FGO/questclear_250_300_400_500.png'    , "picxy": ( 250, 300), 'picwh': ( 150, 200), 'actions': [{'MOUSELEFT': ( 100, 100)}]},
        {'pic':'FGO/again_1740_1370_1820_1450.png'     , "picxy": (1740,1370), 'picwh': (  80,  80), 'actions': [{'MOUSELEFT': ( -10, 100)}]},
    ]
    skipping_cv(log_overlay, pic_overlay, hwnd, pic_list)

def FGO(hwnd, log_overlay, pic_overlay):
    _, active_window = get_window_title(hwnd)
    title = f"{active_window} ; 战斗"
    log_overlay.update_title(title)
    while True:
        hwnd_x, active_window = get_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            mainquest(hwnd, log_overlay, pic_overlay)
        elif is_key_pressed("["):
            capture_mode(hwnd, log_overlay)
        time.sleep(0.2)
