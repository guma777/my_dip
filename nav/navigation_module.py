import cv2

class NavigationModule:
    def __init__(self):
        pass

    def get_direction(self, detections, frame_width):
        left_count = 0
        right_count = 0
        center_zone = frame_width * 0.1  # 10% центра считаем нейтральной зоной

        for obj in detections:
            _, x_min, _, x_max, _, _ = obj  # Проверь, что detections реально в таком формате

            center_x = (x_min + x_max) // 2  # Центр объекта

            if center_x < (frame_width // 2 - center_zone):  # Чётко левее центра
                left_count += 1
            elif center_x > (frame_width // 2 + center_zone):  # Чётко правее центра
                right_count += 1

        if left_count > right_count:
            return "Move LEFT!"
        elif right_count > left_count:
            return "Move RIGHT!"
        else:
            return "Stop!"  # Либо можно вернуть "Hold Position" или что-то другое
