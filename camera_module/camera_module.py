import cv2

class CameraModule:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Ошибка: Не удалось получить кадр с камеры")
            return None
        return frame

    def release(self):
        self.cap.release()