import cv2
import numpy as np
def main():
    
    #pic_list = [
    #    'cap/20250622_161711_0.png',
    #    'cap/20250622_161712_1.png',
    #    'cap/20250622_161712_2.png',
    #    'cap/20250622_161712_3.png',
    #    'cap/20250622_161712_4.png',
    #    'cap/20250622_161713_5.png',
    #    'cap/20250622_161713_6.png',
    #    'cap/20250622_161713_7.png',
    #    'cap/20250622_161714_8.png',
    #    'cap/20250622_161714_9.png',
    #    'cap/20250622_161714_10.png',
    #    'cap/20250622_161715_11.png',
    #    'cap/20250622_161715_12.png',
    #    'cap/20250622_161715_13.png',
    #    'cap/20250622_161715_14.png',
    #    'cap/20250622_161716_15.png',
    #    'cap/20250622_161716_16.png',
    #    'cap/20250622_161716_17.png',
    #    'cap/20250622_161717_18.png',
    #    'cap/20250622_161717_19.png',
    #    ]
    #
    #x1, y1 = 2202, 1650
    #x2, y2 = 2248, 1684
    pic_list = [
        'cap/20250622_163537.png',
        'cap/20250622_163642.png',
        'cap/20250622_163747.png',
        'cap/20250622_163834.png',
        'cap/20250622_163835.png',
    ]
    x1, y1 = 2138, 1248
    x2, y2 = 2210, 1342

    image = cv2.imread(pic_list[0], cv2.IMREAD_UNCHANGED)
    diff = np.zeros(image.shape[:2])

    num = len(pic_list)
    i = 0
    for i in range(num-1):
        for j in range(i+1,num):
            image1 = cv2.imread(pic_list[i], cv2.IMREAD_UNCHANGED)
            image2 = cv2.imread(pic_list[j], cv2.IMREAD_UNCHANGED)
            diff_12 = cv2.absdiff(image1, image2)
            diff_12[diff_12 < 2] = 0
            diff += diff_12
    diff = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    cv2.imwrite('cap/diff.png', diff)

    diff_clip = diff[y1:y2, x1:x2]
    alpha = np.zeros_like(diff_clip, dtype=np.uint8)
    alpha[diff_clip<2] = 255

    clip = image[y1:y2, x1:x2]
    print(clip.shape, alpha.shape)
    bgra_image = cv2.merge([clip, clip, clip, alpha])
    cv2.imwrite(f'cap/clip_{x1}_{y1}_{x2}_{y2}.png', bgra_image)
if __name__ == "__main__":
    main()