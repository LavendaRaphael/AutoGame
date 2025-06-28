import time
import sys
import threading
from ctypes import windll
from winlib import get_foreground_window_title, is_key_pressed, LogOverlay, fishing, skipping
import logging

# 配置日志记录
logging.basicConfig(
    filename='debug.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# 游戏模式
def nikky(hwnd, overlay, active_window):
    txt = f"{active_window} [ 钓鱼 ; 跳过"
    overlay.update_text(txt)
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed("["):
            fishing(overlay)
            overlay.update_text(txt)
        elif is_key_pressed(";"):
            skipping(overlay, skip_key=['F'])
            overlay.update_text(txt)
        time.sleep(0.2)

def mihoyo(hwnd, overlay, active_window):
    txt = f"{active_window} ; 跳过"
    overlay.update_text(txt)
    while True:
        hwnd_x, active_window = get_foreground_window_title()
        if hwnd_x != hwnd:
            break
        if is_key_pressed(";"):
            skipping(overlay, skip_key=['MOUSELEFT','1'])
            overlay.update_text(txt)
        time.sleep(0.2)

# 主要执行函数
def game_script_thread(overlay):
    
    while True:
        hwnd, active_window = get_foreground_window_title()
        if active_window == "无限暖暖  ":
            nikky(hwnd, overlay, active_window)
        elif active_window in ["崩坏：星穹铁道","绝区零", '重返未来：1999']:
            mihoyo(hwnd, overlay, active_window)
        else:
            overlay.update_text(f"当前窗口: {active_window}")
            logging.info(f"当前窗口: {active_window}")
        time.sleep(1)

def main():
    if not windll.shell32.IsUserAnAdmin():
        windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        return

    overlay = LogOverlay(None)
    # 将 overlay 实例传递给子线程
    script_thread = threading.Thread(target=game_script_thread, args=(overlay,), daemon=True)
    script_thread.start()
    overlay.root.mainloop()

if __name__ == "__main__":
    main()