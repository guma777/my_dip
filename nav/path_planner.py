from typing import List, Tuple

class PathPlanner:
    def __init__(self, frame_width=640, frame_height=480):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.previous_positions = {}
        self.object_directions = {}

    def get_direction(self, detections):
        self.update_trajectories(detections)

        frame_width = self.frame_width
        frame_height = self.frame_height
        center_x = frame_width // 2

        nearest_center_distance = float('inf')
        left_zone = (0, 0, frame_width // 3, frame_height)
        right_zone = (2 * frame_width // 3, 0, frame_width, frame_height)

        left_distance = self._zone_min_distance(detections, zone='left')
        right_distance = self._zone_min_distance(detections, zone='right')

        for det in detections:
            label, xmin, ymin, xmax, ymax, conf = det
            distance = self.estimate_distance((ymin, ymax), frame_height)
            box_center = (xmin + xmax) / 2

            # Центр опасности
            if abs(box_center - center_x) < 100:
                if distance < 1.2:
                    print(f"[!] В центре близко: {label}, {distance} м")
                    return 'stop'

            # Разделённые реакции
            if label == 'car' and distance < 2:
                return 'stop'
            if label in ['dog', 'cat'] and distance < 1:
                return 'stop'

        if left_distance < 2 and right_distance < 2:
            return 'stop'
        elif left_distance > right_distance:
            return 'Turn LEFT'
        else:
            return 'Turn RIGHT'

    def update_trajectories(self, detections):
        for label, x_min, y_min, x_max, y_max, conf in detections:
            center_x = (x_min + x_max) / 2
            object_id = f"{label}_{round(x_min)}"

            if object_id in self.previous_positions:
                delta = center_x - self.previous_positions[object_id]
                if delta > 15:
                    self.object_directions[object_id] = 'right'
                elif delta < -15:
                    self.object_directions[object_id] = 'left'
                else:
                    self.object_directions[object_id] = 'still'

            self.previous_positions[object_id] = center_x

    def _zone_min_distance(self, detections, zone='left'):
        min_dist = float('inf')
        for det in detections:
            label, xmin, ymin, xmax, ymax, conf = det
            distance = self.estimate_distance((ymin, ymax), self.frame_height)
            if zone == 'left' and xmax < self.frame_width // 3:
                min_dist = min(min_dist, distance)
            elif zone == 'right' and xmin > 2 * self.frame_width // 3:
                min_dist = min(min_dist, distance)
        return min_dist

    def estimate_distance(self, box_y, frame_height):
        ymin, ymax = box_y
        box_height = ymax - ymin
        if box_height == 0:
            return float('inf')
        return round((frame_height * 2.0) / box_height, 2)
