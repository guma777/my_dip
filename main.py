import cv2
from camera_module import CameraModule
from yolo_pac import YOLOModule
from nav import NavigationModule

def main():
    # Инициализация модулей
    camera = CameraModule()
    yolo = YOLOModule("yolo_pac/yolo11n.pt")  # Убедись, что путь к модели правильный
    nav = NavigationModule()

    # Открытие камеры
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Распознавание объектов
        detections = yolo.detect_objects(frame)

        # Получение направления движения
        direction = nav.get_direction(detections, frame.shape[1])

        # Отображение результата
        frame = nav.process_objects(frame, detections)
        frame = nav.display_direction(frame, direction)

        cv2.imshow("Navigation System", frame)

        # Выход по клавише 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()