import cv2
from camera_module.camera_module import CameraModule
from yolo_pac.yolo_module import YOLOModule
from nav.navigation_module import NavigationModule

# Инициализация модулей
camera = CameraModule()
yolo = YOLOModule("yolo_pac/yolo11n.pt")
nav = NavigationModule()

# Позволяем окну менять размер и устанавливаем стартовый размер
cv2.namedWindow("Navigation System", cv2.WINDOW_NORMAL)


while True:
    frame = camera.get_frame()
    if frame is None:
        break

    frame_width = frame.shape[1]

    # Обнаружение объектов
    detections = yolo.detect_objects(frame)

    # Определение направления
    direction = nav.get_direction(detections, frame_width)

    # Отрисовка объектов
    frame = yolo.draw_boxes(frame, detections)

    # Рисуем границы зон
    left_border = frame_width // 3
    right_border = 2 * (frame_width // 3)
    cv2.line(frame, (left_border, 0), (left_border, frame.shape[0]), (255, 0, 0), 2)
    cv2.line(frame, (right_border, 0), (right_border, frame.shape[0]), (255, 0, 0), 2)

    # Отображение текста направления
    cv2.putText(frame, direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    # Вывод кадра
    cv2.imshow("Navigation System", frame)

    # Выход по 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Завершаем работу
camera.release()
cv2.destroyAllWindows()
