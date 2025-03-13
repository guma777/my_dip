import cv2

class CameraModule:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            print("Ошибка: Не удалось открыть камеру")
            exit(1)  # Прекращаем выполнение, если камера недоступна

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Ошибка: Не удалось получить кадр с камеры")
            return None
        return frame.copy()  # Возвращаем копию кадра, чтобы избежать кеширования

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()  # Закрываем все окна OpenCV