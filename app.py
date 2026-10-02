import cv2

from src.vision.pose_detector import PoseDetector
from src.vision.bed_detector import BedDetector
from src.vision.feature_extractor import FeatureExtractor
from config.settings import *
from src.state_machine.activity_fsm import ActivityFSM
from src.agent.memory import ActivityMemory
from src.logger import get_logger
logger = get_logger(__name__)

def main():

    logger.info("Start the pipeline")

    video = cv2.VideoCapture(
        VIDEO_PATH
    )

    pose_detector = PoseDetector()

    bed_detector = BedDetector()

    feature_extractor = FeatureExtractor()

    fsm = ActivityFSM()

    memory = ActivityMemory()


    while True:

        success, frame = video.read()

        if not success:
            break

        result = pose_detector.detect(frame)

        if result.keypoints is not None:

            kp = (
                result.keypoints.xy[0]
                .cpu()
                .numpy()
            )

            center_x = int(kp[:, 0].mean())

            center_y = int(kp[:, 1].mean())

            inside_bed = (
                bed_detector.is_inside_bed(
                    center_x,
                    center_y
                )
            )

            features = (
                feature_extractor
                .calculate_features(
                    kp,
                    inside_bed
                )
            )

            state = fsm.update(
                features
            )

            memory.add(
                state.value
            )

            cv2.putText(
                frame,
                state.value,
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        cv2.imshow(
            "Activity Recognition",
            frame
        )

        if cv2.waitKey(1) == 27:
            break

    video.release()

    cv2.destroyAllWindows()

if __name__=="__main__":
    main()