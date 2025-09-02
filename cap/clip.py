import cv2
import numpy as np
import os

def main():
    pic_list = os.listdir('cap/clip/')
    #pic_list = pic_list[:5]
    for i in range(len(pic_list)):
        pic_list[i] = 'cap/clip/'+pic_list[i]
    x1, y1 = 2690, 670
    w, h = 80, 60
    x2 = x1+w
    y2 = y1+h

    image = cv2.imread(pic_list[0], cv2.IMREAD_UNCHANGED)
    diff = np.zeros(image.shape[:2])

    num = len(pic_list)
    i = 0
    for i in range(num-1):
        for j in range(i+1,num):
            image1 = cv2.imread(pic_list[i], cv2.IMREAD_UNCHANGED)
            image2 = cv2.imread(pic_list[j], cv2.IMREAD_UNCHANGED)
            diff_12 = cv2.absdiff(image1, image2)
            _, diff_12 = cv2.threshold(diff_12, 2, 255, cv2.THRESH_TOZERO)
            diff += diff_12
    _, diff = cv2.threshold(diff, 255, 255, cv2.THRESH_TRUNC)
    diff = diff.astype(np.uint8)
    cv2.imwrite('cap/diff.png', diff)

    diff_clip = diff[y1:y2, x1:x2]
    _, alpha = cv2.threshold(diff_clip, 2, 255, cv2.THRESH_BINARY_INV)
    alpha = alpha.astype(np.uint8)

    clip = image[y1:y2, x1:x2]
    print(clip.shape, alpha.shape)
    bgra_image = cv2.merge([clip, clip, clip, alpha])
    cv2.imwrite(f'cap/clip_{x1}_{y1}_{w}_{h}.png', bgra_image)

if __name__ == "__main__":
    main()