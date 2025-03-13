import cv2

class YOLOModule:
    def __init__(self, model_path='yolo_pac/yolo11n.pt'):
        self.model_path = model_path
        print(f"Модель YOLO загружена из {self.model_path}")

    def detect_objects(self, frame):
        # Имитация детекции (замени на реальный код)
        detections = [
            ('person', 50, 50, 100, 200, 0.95),
            ('car', 120, 80, 220, 160, 0.87)  # Исправлены координаты
        ]
        return detections

    def draw_boxes(self, frame, detections):
        for detection in detections:
            label, x_min, y_min, x_max, y_max, confidence = detection

            x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            text = f"{label} ({confidence:.2f})"
            cv2.putText(frame, text, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame