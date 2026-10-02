from src.state_machine.states import ActivityState
from config.settings import *

class ActivityFSM:

    def __init__(self):

        self.current_state = ActivityState.UNKNOWN

    def update(self, features):

        angle = features["body_angle"]

        speed = features["speed"]

        inside_bed = features["inside_bed"]

        if inside_bed and angle < 25:

            self.current_state = (
                ActivityState.LYING_IN_BED
            )

        elif inside_bed and angle > 60:

            self.current_state = (
                ActivityState.SITTING_ON_BED
            )

        elif not inside_bed and speed < 10:

            self.current_state = (
                ActivityState.STANDING
            )

        elif not inside_bed and speed >= 10:

            self.current_state = (
                ActivityState.WALKING
            )

        elif not inside_bed:

            self.current_state = (
                ActivityState.OUT_OF_BED
            )

        return self.current_state