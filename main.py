import cv2
from camera_module import CameraModule
from yolo_pac import YOLOModule
from nav import NavigationModule

# Инициализация модулей
yolo = YOLOModule("yolo_pac/yolo11n.pt")
nav = NavigationModule()

# Захват видео с камеры
cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_width = frame.shape[1]

    # Обнаружение объектов
    detections = yolo.detect_objects(frame)

    # Определение направления
    direction = nav.get_direction(detections, frame_width)

    # Рисуем границы для левой, центральной и правой зоны
    left_border = frame_width // 3
    right_border = 2 * (frame_width // 3)
    cv2.line(frame, (left_border, 0), (left_border, frame.shape[0]), (255, 0, 0), 2)
    cv2.line(frame, (right_border, 0), (right_border, frame.shape[0]), (255, 0, 0), 2)

    # Отображение детекций
    for obj in detections:
        label, x1, y1, x2, y2, confidence = obj

        # Рисуем рамку
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{label} ({confidence:.2f})", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Вывод координат объекта
        cv2.putText(frame, f"x min = {x1}", (x1, y1 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, f"x max = {x2}", (x1, y1 + 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, f"y min = {y1}", (x1, y1 + 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(frame, f"y max = {y2}", (x1, y1 + 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Вывод направления движения
    cv2.putText(frame, direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 3)

    # Отображение кадра
    cv2.imshow("Navigation System", frame)

    # Выход по 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()