import cv2

class NavigationModule:
    def __init__(self):
        pass

    def get_direction(self, detections, frame_width):
        left_count = 0
        right_count = 0

        # Разделяем объекты на левые и правые
        for obj in detections:
            _, x_min, _, x_max, _, _ = obj

            if x_max < frame_width // 2:
                left_count += 1  # Препятствия слева
            else:
                right_count += 1  # Препятствия справа

        # Логика выбора направления
        if left_count < right_count:
            return "Move LEFT!"
        elif right_count < left_count:
            return "Move RIGHT!"
        else:
            return "Stop!"

    def process_objects(self, frame, detections):
        for obj in detections:
            label, x_min, y_min, x_max, y_max, confidence = obj

            # Отрисовка рамки
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            # Текстовая метка
            text = f"{label} ({confidence:.2f})"
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
            cv2.rectangle(frame, (x_min, y_min - 20), (x_min + text_size[0] + 5, y_min), (0, 0, 0), -1)
            cv2.putText(frame, text, (x_min, y_min - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

        return frame

    def display_direction(self, frame, action):
        text_size = cv2.getTextSize(action, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        cv2.rectangle(frame, (45, 80), (55 + text_size[0], 110), (0, 0, 0), -1)  # Чёрный фон
        cv2.putText(frame, action, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        return frame