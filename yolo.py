from ultralytics import YOLO

model = YOLO("yolo11n.pt")  # 加载预训练模型

if __name__ == '__main__':
    model.train(
        data='yolo/icon.yml',
        epochs = 300,
        rect = True,
        imgsz = 2896,
    )
