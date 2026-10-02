import math
import numpy as np


class FeatureExtractor:

    def __init__(self):

        self.previous_center = None

    # --------------------------------------------------
    # Get a keypoint
    # --------------------------------------------------

    def point(self, keypoints, index):

        x, y = keypoints[index]

        return np.array([x, y], dtype=float)

    # --------------------------------------------------
    # Calculate midpoint
    # --------------------------------------------------

    def midpoint(self, p1, p2):

        return (p1 + p2) / 2

    # --------------------------------------------------
    # Calculate body angle relative to vertical
    #
    # 0 degrees  = vertical
    # 90 degrees = horizontal
    # --------------------------------------------------

    def calculate_body_angle(
        self,
        shoulder_center,
        hip_center
    ):

        dx = hip_center[0] - shoulder_center[0]

        dy = hip_center[1] - shoulder_center[1]

        angle = math.degrees(
            math.atan2(
                abs(dx),
                abs(dy)
            )
        )

        return angle

    # --------------------------------------------------
    # Calculate joint angle
    #
    # Example:
    # hip -> knee -> ankle
    # --------------------------------------------------

    def calculate_joint_angle(
        self,
        a,
        b,
        c
    ):

        ba = a - b

        bc = c - b

        norm_ba = np.linalg.norm(ba)

        norm_bc = np.linalg.norm(bc)

        if norm_ba == 0 or norm_bc == 0:

            return 0.0

        cosine_angle = np.dot(
            ba,
            bc
        ) / (
            norm_ba *
            norm_bc
        )

        cosine_angle = np.clip(
            cosine_angle,
            -1.0,
            1.0
        )

        angle = math.degrees(
            math.acos(
                cosine_angle
            )
        )

        return angle

    # --------------------------------------------------
    # Calculate features
    # --------------------------------------------------

    def calculate_features(
        self,
        keypoints,
        inside_bed
    ):

        # ==================================================
        # BODY POINTS
        # ==================================================

        left_shoulder = self.point(
            keypoints,
            5
        )

        right_shoulder = self.point(
            keypoints,
            6
        )

        left_hip = self.point(
            keypoints,
            11
        )

        right_hip = self.point(
            keypoints,
            12
        )

        left_knee = self.point(
            keypoints,
            13
        )

        right_knee = self.point(
            keypoints,
            14
        )

        left_ankle = self.point(
            keypoints,
            15
        )

        right_ankle = self.point(
            keypoints,
            16
        )

        # ==================================================
        # BODY MIDPOINTS
        # ==================================================

        shoulder_center = self.midpoint(
            left_shoulder,
            right_shoulder
        )

        hip_center = self.midpoint(
            left_hip,
            right_hip
        )

        knee_center = self.midpoint(
            left_knee,
            right_knee
        )

        ankle_center = self.midpoint(
            left_ankle,
            right_ankle
        )

        # ==================================================
        # BODY ANGLE
        # ==================================================

        body_angle = self.calculate_body_angle(
            shoulder_center,
            hip_center
        )

        # ==================================================
        # KNEE ANGLES
        # ==================================================

        left_knee_angle = self.calculate_joint_angle(
            left_hip,
            left_knee,
            left_ankle
        )

        right_knee_angle = self.calculate_joint_angle(
            right_hip,
            right_knee,
            right_ankle
        )

        knee_angle = (
            left_knee_angle +
            right_knee_angle
        ) / 2

        # ==================================================
        # BODY HEIGHT
        # ==================================================

        body_height = np.linalg.norm(
            ankle_center -
            shoulder_center
        )

        # ==================================================
        # BODY WIDTH
        # ==================================================

        body_width = np.linalg.norm(
            shoulder_center -
            hip_center
        )

        # ==================================================
        # MOVEMENT
        # ==================================================

        center = hip_center

        speed = 0.0

        if self.previous_center is not None:

            speed = np.linalg.norm(
                center -
                self.previous_center
            )

        self.previous_center = center

        # ==================================================
        # RETURN FEATURES
        # ==================================================

        return {

            "body_angle": body_angle,

            "left_knee_angle": left_knee_angle,

            "right_knee_angle": right_knee_angle,

            "knee_angle": knee_angle,

            "body_height": body_height,

            "body_width": body_width,

            "speed": speed,

            "inside_bed": inside_bed,

            "shoulder_center": shoulder_center,

            "hip_center": hip_center,

            "knee_center": knee_center,

            "ankle_center": ankle_center
        }