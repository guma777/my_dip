import cv2

class YOLOModule:
    def __init__(self, model_path):

        self.model_path = 'yolo_pac/yolo11n.pt'
        print(f"Модель YOLO загружена из {model_path}")

    def detect_objects(self, frame):
        # Имитация распознавания объектов (замени на свой код)
        detections = [
            ('person', 50, 50, 100, 200, 0.95),
            ('car', 200, 100, 150, 100, 0.87)
        ]
        return detections

    def draw_boxes(self, frame, detections):
        for detection in detections:
            label, x, y, w, h, confidence = detection

            x, y, w, h = int(x), int(y), int(w), int(h)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            text = f"{label} ({confidence:.2f})"
            cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        return frame