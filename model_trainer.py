import torch
from ultralytics import YOLO
import multiprocessing

if __name__ == '__main__':
    multiprocessing.freeze_support()

    # Use GPU if available, otherwise CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load the pre-trained YOLOv8 model
    model = YOLO("yolov8n.pt")

    # Train with your custom dataset
    results = model.train(
        data="D:/Pycharm Projects/New folder/data.yaml",
        epochs=5,
        imgsz=640,
        batch=32,
        device=device,
        amp=True,
        workers=4,
        save_period=1
    )

    # Save the trained model
    model.save('custom_traffic_model.pt')