import cv2
import time
import serial
from camera_module.camera_module import CameraModule
from yolo_pac.yolo_module import YOLOModule
from nav.navigation_module import NavigationModule

# Инициализация камеры, YOLO, навигации
camera = CameraModule()
yolo = YOLOModule('yolo_pac/yolo11s.pt')
navigator = NavigationModule(frame_width=640, frame_height=480)

# Инициализация Arduino через USB (укажи свой COM порт)
#arduino = serial.Serial('COM3', 9600)
time.sleep(2)  # Ждём подключения

# Карта команд для Arduino
command_map = {
    "Move FORWARD": b'F',
    "Turn LEFT": b'L',
    "Turn RIGHT": b'R',
    "stop": b'S'
}

def draw_arrow(frame, direction):
    h, w = frame.shape[:2]
    center = (w // 2, h - 50)

    if direction == "Move FORWARD":
        endpoint = (center[0], center[1] - 100)
        color = (0, 255, 0)
    elif direction == "Turn LEFT":
        endpoint = (center[0] - 100, center[1] - 50)
        color = (255, 255, 0)
    elif direction == "Turn RIGHT":
        endpoint = (center[0] + 100, center[1] - 50)
        color = (255, 255, 0)
    else:  # stop
        endpoint = center
        color = (0, 0, 255)

    cv2.arrowedLine(frame, center, endpoint, color, 5, tipLength=0.5)
    return frame

# Основной цикл
while True:
    frame = camera.get_frame()
    if frame is None:
        break

    frame_height, frame_width = frame.shape[:2]
    detections = yolo.detect_objects(frame)

    direction = navigator.get_direction(detections, frame_width, frame_height)

    # Отправляем команду на Arduino
   ##arduino.write(command_map[direction])

    frame = yolo.draw_boxes(frame, detections)
    frame = draw_arrow(frame, direction)

    # Показываем направление на экране
    cv2.putText(frame, direction, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Smart Navigation", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
#arduino.close()
cv2.destroyAllWindows()
