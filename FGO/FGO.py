from winlib import get_window_title, is_key_pressed, skipping_cv, capture_mode
import time

def FGO(hwnd, log_overlay, pic_overlay):
    _, active_window = get_window_title(hwnd)
    title = f"{active_window} ; 战斗"
    log_overlay.update_title(title)
    while True:
        hwnd_x, active_window = get_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            pic_list = [
                {'pic':'FGO/mainquest_1770_450_1850_550.png'   , "picxy": (1770, 450), 'picwh': ( 80,100), 'key': 'MOUSELEFT', "shift": [(100,100)]},
                {'pic':'FGO/skipyes_1800_1320_1970_1400.png'   , "picxy": (1800,1320), 'picwh': (170, 80), 'key': 'MOUSELEFT', "shift": [(100,100)]},
                {'pic':'FGO/skip_2550_125_2880_250.png'        , "picxy": (2550, 125), 'picwh': (330,125), 'key': 'MOUSELEFT', "shift": [(100,100)]},
                {'pic':'FGO/friendselect_1680_340_1800_450.png', "picxy": (1680, 340), 'picwh': (120,110), 'key': 'MOUSELEFT', "shift": [(100,200)]},
                {'pic':'FGO/teamclose_1330_1400_1400_1500.png' , "picxy": (1330,1400), 'picwh': ( 70,100), 'key': 'MOUSELEFT', "shift": [(100,100)]},
                {'pic':'FGO/teamauto_1900_1420_1970_1500.png'  , "picxy": (1900,1420), 'picwh': ( 70, 80), 'key': 'MOUSELEFT', "shift": [(100,100)]},
                {'pic':'FGO/teamok_2580_1580_2650_1650.png'    , "picxy": (2580,1580), 'picwh': ( 70, 70), 'key': 'MOUSELEFT', "shift": [(100,100)]},
                {'pic':'FGO/teamend_600_1580_750_1680.png'     , "picxy": ( 600,1580), 'picwh': (150,100), 'key': 'MOUSELEFT', "shift": [(2000,100)]},
                {'pic':'FGO/attack_2600_1580_2800_1680.png'    , "picxy": (2600,1580), 'picwh': (200,100), 'key': 'MOUSELEFT', "shift": [(-200,-200)]},
                {'pic':'FGO/attackback_2650_1600_2800_1680.png', "picxy": (2650,1600), 'picwh': (150, 80), 'key': 'MOUSELEFT', "shift": [(-100,-400),(-700,-400),(-1300,-400)]},
                {'pic':'FGO/getzhanli_2400_1500_2550_1600.png' , "picxy": (2400,1500), 'picwh': (150,100), 'key': 'MOUSELEFT', "shift": [(-100,100)]},
                {'pic':'FGO/getjiban_180_480_260_550.png'      , "picxy": ( 180, 480), 'picwh': ( 80, 70), 'key': 'MOUSELEFT', "shift": [(100,100)]},
                {'pic':'FGO/getexp_1470_530_1550_600.png'      , "picxy": (1470, 530), 'picwh': ( 80, 70), 'key': 'MOUSELEFT', "shift": [(100,100)]},
                #{'pic':'FGO/friendapply_2600_280_2750_350.png' , "picxy": (2600, 280), 'picwh': (150, 70), 'key': 'MOUSELEFT', "shift": [(100,100)]},
                {'pic':'FGO/questclear_250_300_400_500.png'    , "picxy": ( 250, 300), 'picwh': (150,200), 'key': 'MOUSELEFT', "shift": [(100,100)]},
                {'pic':'FGO/again_1740_1370_1820_1450.png'     , "picxy": (1740,1370), 'picwh': ( 80, 80), 'key': 'MOUSELEFT', "shift": [(-10,100)]},
            ]
            skipping_cv(log_overlay, pic_overlay, hwnd, pic_list)
        elif is_key_pressed("["):
            capture_mode(hwnd, log_overlay)
        time.sleep(0.2)
