import cv2
import numpy as np

if __name__ == "__main__":
    
    pic_list = [
        'cap/20250615_152952.png',
        'cap/20250615_153237.png',
        'cap/20250615_153253.png',
        'cap/20250615_153727.png',
        ]
    
    image = cv2.imread(pic_list[0], cv2.IMREAD_UNCHANGED)
    diff = np.zeros(image.shape[:2])

    num = len(pic_list)
    i = 0
    for i in range(num-1):
        for j in range(i+1,num):
            image1 = cv2.imread(pic_list[i], cv2.IMREAD_UNCHANGED)
            image2 = cv2.imread(pic_list[j], cv2.IMREAD_UNCHANGED)
            image1_g = cv2.cvtColor(image1, cv2.COLOR_BGRA2GRAY)
            image2_g = cv2.cvtColor(image2, cv2.COLOR_BGRA2GRAY)
            diff_12 = cv2.absdiff(image1_g, image2_g)
            diff_12[diff_12 < 2] = 0
            diff += diff_12

    cv2.imwrite('cap/diff.png', diff)

    x1, y1 = 192, 52
    x2, y2 = 450, 120

    diff_clip = diff[y1:y2, x1:x2]
    alpha = np.zeros_like(diff_clip)
    alpha[diff_clip<2] = 255

    clip = image[y1:y2, x1:x2]
    clip[:, :, 3] = alpha
    cv2.imwrite('cap/clip.png', clip)