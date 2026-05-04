from winlib import get_window_title, is_key_pressed, skipping, capture_mode
import time

def juqing(hwnd, log_overlay, pic_overlay):
    mode = log_overlay.mode
    log_overlay.update(mode = "剧情模式 退出 ]")
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
            "picxy": (2352,1704), 'picwh': (40+2560-2352,40+1720-1704), 
            'actions': [
                {'press':'F'}
            ]
        },
        {
            'pic':'InfinityNikky/pic/yituijiandapei_1330_440_50_50.png', 
            "picxy": (1330,440), 'picwh': (50,50), 
            'actions': [
                {'sleep': 0.5},
                {'click': ('VK_LBUTTON', (270-1330,1650-440))},
                {'sleep': 0.5},
                {'click': ('VK_LBUTTON', (270-1330,1650-440))},
                {'sleep': 0.5},
                {'click': ('VK_LBUTTON', (270-1330,1650-440))},
                {'sleep': 0.5},
                {'click': ('VK_LBUTTON', (270-1330,1650-440))},
            ]
        },
        {
            'pic':'InfinityNikky/pic/tuijiandapei_1530_700_50_50.png', 
            "picxy": (1530,700), 'picwh': (50+1538-1530,50+758-700), 
            'actions': [
                {'sleep': 0.5},
                {'click': ('VK_LBUTTON', (100,50))},
                {'sleep': 0.5},
                {'click': ('VK_LBUTTON', (100,50))},
                {'sleep': 0.5},
            ]
        },
        {
            'pic':'InfinityNikky/pic/tuijiandapei_1530_700_50_50.png', 
            "picxy": (1680,700), 'picwh': (50,50), 
            'actions': [
                {'sleep': 0.5},
                {'click': ('VK_LBUTTON', (270-1530,1650-700))},
                {'sleep': 0.5},
                {'click': ('VK_LBUTTON', (270-1530,1650-700))},
            ]
        },
        {
            'pic':'InfinityNikky/pic/querendapei_160_1670_50_50.png', 
            "picxy": (160,1670), 'picwh': (50,50), 
            'actions': [
                {'sleep': 0.5},
                {'click': ('VK_LBUTTON', (200,30))}
            ]
        },
        {
            'pic':'InfinityNikky/pic/chuansong_2380_1660_50_50.png', 
            "picxy": (2380,1660), 'picwh': (50,50), 
            'actions': [
                {'click': ('VK_LBUTTON', (100,50))}
            ]
        },
    ]
    skipping(log_overlay, pic_overlay, hwnd, pic_list)
    log_overlay.update(mode = mode)

def Nikky(hwnd, log_overlay, pic_overlay):
    log_overlay.update(mode = '剧情 ;')
    while True:
        hwnd_x, active_window = get_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            juqing(hwnd, log_overlay, pic_overlay)
        elif is_key_pressed("["):
            capture_mode(hwnd, log_overlay)
        time.sleep(0.2)

def fishing(log_overlay):
    mode = log_overlay.mode
    log_overlay.update_text(mode = "[钓鱼模式] 拉线 A 退出 ]")
    time.sleep(1)
    while True:
        if is_key_pressed("A"):
            log_overlay.update(mode = "拉线中 F 退出")
            while not is_key_pressed("F"):
                press('MOUSERIGHT')
                time.sleep(0.1)
            log_overlay.update(text = '拉线结束')
        elif is_key_pressed("]"):
            break
        time.sleep(0.1)
    
    log_overlay.update_text(mode = mode)