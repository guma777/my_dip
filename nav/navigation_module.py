import cv2

class NavigationModule:
    def __init__(self):
        pass

    def get_direction(self, detections, frame_width):  # Добавляем frame_width
        left_count = 0
        right_count = 0

        for obj in detections:
            _, x_min, _, x_max, _, _ = obj

            if x_max < frame_width // 2:
                left_count += 1
            else:
                right_count += 1

        if left_count < right_count:
            return "Move LEFT!"
        elif right_count < left_count:
            return "Move RIGHT!"
        else:
            return "Stop!"