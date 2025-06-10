from .path_planner import PathPlanner

class NavigationModule:
    def __init__(self, frame_width=640, frame_height=480):
        self.planner = PathPlanner(frame_width, frame_height)

    def get_direction(self, detections, frame_width, frame_height):
        # Можно не передавать frame_width/height — уже есть в self.planner
        return self.planner.get_direction(detections)
