from ultralytics import YOLO


class PoseDetector:

    def __init__(self):
        self.model = YOLO("yolov8n-pose.pt")

    def detect(self, frame):

        results = self.model(frame)

        return results[0]