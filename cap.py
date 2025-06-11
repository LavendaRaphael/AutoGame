import cv2
import numpy as np
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":

    image = cv2.imread('cap/diff.png', cv2.IMREAD_UNCHANGED)
    print(image.shape)
    
    x1, y1 = 2204, 1652
    x2, y2 = 2246, 1684
    diff_cap = image[y1:y2, x1:x2]
    print(diff_cap)
    cv2.imwrite("cap/diff_cap.png", diff_cap)

    for i in range(5,40,5):
        image_tmp = np.where(image > i, 255, 0)
        cv2.imwrite(f"cap/image_{i}.png", image_tmp)
        cap_tmp = image_tmp[y1:y2, x1:x2]
        cv2.imwrite(f"cap/cap_{i}.png", cap_tmp)
    