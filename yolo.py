from ultralytics import YOLO

model = YOLO("yolo11n.pt")  # 加载预训练模型

if __name__ == '__main__':
    model.train(
        data='FGO/yolo/icon.yml',
        epochs = 600,
        rect = True,
    )
