import cv2
import numpy as np

if __name__ == "__main__":
    pic1 = cv2.imread('cap/test1.png', cv2.IMREAD_UNCHANGED)
    pic2 = cv2.imread('cap/test2.png', cv2.IMREAD_UNCHANGED)
    pic1_g = cv2.cvtColor(pic1, cv2.COLOR_BGRA2GRAY)
    pic2_g = cv2.cvtColor(pic2, cv2.COLOR_BGRA2GRAY)
    diff = cv2.absdiff(pic1_g, pic2_g)
    cv2.imwrite("cap/diff.png", diff)

    x1, y1 = 2204, 1652
    x2, y2 = 2246, 1684
    mask = diff[y1:y2, x1:x2]
    
    # 创建 alpha 通道：差异设为 255，不变为 0
    alpha = np.zeros_like(mask)
    alpha[mask >= 80] = 255

    # 提取原图像片段并添加 alpha
    cap = pic1[y1:y2, x1:x2].copy()
    if cap.shape[2] == 3:
        cap = cv2.cvtColor(cap, cv2.COLOR_BGR2BGRA)
    cap[:, :, 3] = alpha

    cv2.imwrite('cap/cap.png', cap)
    
    cap = cv2.imread('cap/cap.png', cv2.IMREAD_UNCHANGED)
    cap_g = cv2.cvtColor(cap, cv2.COLOR_BGRA2GRAY)
    result = cv2.matchTemplate(pic1_g, cap_g, cv2.TM_CCORR_NORMED, mask=alpha)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(min_val, min_loc)
    print(max_val, max_loc)