import cv2
import torch
from ultralytics import YOLO

class YOLOModule:
    def __init__(self, model_path='yolo_pac/yolo11n.pt'):
        self.model = YOLO(model_path)  # Загружаем модель
        print(f"Модель YOLO загружена из {model_path}")

    def detect_objects(self, frame):
        results = self.model(frame)  # Запускаем модель на изображении

        detections = []
        for result in results:
            for box in result.boxes.data:
                x_min, y_min, x_max, y_max, confidence, class_id = box.tolist()
                label = self.model.names[int(class_id)]  # Получаем имя класса
                detections.append((label, x_min, y_min, x_max, y_max, confidence))

        return detections

    def draw_boxes(self, frame, detections):
        for detection in detections:
            label, x_min, y_min, x_max, y_max, confidence = detection

            x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            text = f"{label} ({confidence:.2f})"
            cv2.putText(frame, text, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame
