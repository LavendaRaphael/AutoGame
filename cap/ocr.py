import cv2
from rapidocr_onnxruntime import RapidOCR

def main():
    
    engine = RapidOCR()

    image = cv2.imread('cap/20260313_225316.png', cv2.IMREAD_UNCHANGED)
    result, _ = engine(image)
    if result:
        for item in result:
            print(item)

    x1, y1 = 60, 90
    x2, y2 = 130, 130
    w, h = x2-x1, y2-y1
    print(w, h)
    roi = image[y1:y2, x1:x2]
    result, _ = engine(roi)
    if result:
        for item in result:
            print(item)
            
if __name__ == "__main__":
    main()