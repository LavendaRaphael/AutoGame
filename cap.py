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
    diff_cap = diff[y1:y2, x1:x2]
    cv2.imwrite("cap/diff_cap.png", diff_cap)

    ## 创建 alpha 通道：差异设为 255，不变为 0
    #alpha = np.zeros_like(diff_cap)
    #alpha[diff_cap >= 80] = 255
#
    ## 提取原图像片段并添加 alpha
    #cap = pic1[y1:y2, x1:x2].copy()
    #if cap.shape[2] == 3:
    #    cap = cv2.cvtColor(cap, cv2.COLOR_BGR2BGRA)
    #cap[:, :, 3] = alpha
    #cv2.imwrite('cap/cap.png', cap)
    
    pic3 = cv2.imread('cap/test3.png', cv2.IMREAD_UNCHANGED)
    pic4 = cv2.imread('cap/test4.png', cv2.IMREAD_UNCHANGED)
    pic3_g = cv2.cvtColor(pic3, cv2.COLOR_BGRA2GRAY)
    pic4_g = cv2.cvtColor(pic4, cv2.COLOR_BGRA2GRAY)
    diff_2 = cv2.absdiff(pic3_g, pic4_g)
    cv2.imwrite("cap/diff_2.png", diff_2)

    result = cv2.matchTemplate(diff, diff_cap, cv2.TM_CCORR_NORMED)
    print(cv2.minMaxLoc(result))
    
    result2 = cv2.matchTemplate(diff_2, diff_cap, cv2.TM_CCORR_NORMED)
    print(cv2.minMaxLoc(result2))

