from ultralytics import YOLO
import cv2

#model = YOLO("FGO/best.pt")
model = YOLO("runs/detect/train4/weights/last.pt")
image = cv2.imread('cap/20250825_234711.png', cv2.IMREAD_UNCHANGED)
image_bgr = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
results = model.predict(image_bgr, conf=0.5)
if len(results[0].boxes)>0:
    box = results[0].boxes[0]
    x1,y1,x2,y2 = box.xyxy.tolist()[0]
    loc = (x1, y1)
    w = x2 - x1
    h = y2 - y1
    conf = box.conf.item()
    print(x1, y2, w, h, conf)