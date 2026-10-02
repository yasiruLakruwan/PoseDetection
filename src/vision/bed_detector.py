from config.settings import *

class BedDetector:

    def __init__(self):
        self.bed_roi = BED_ROI
        
    def is_inside_bed(self, x, y):

        x1, y1, x2, y2 = self.bed_roi

        return (
            x1 <= x <= x2 and
            y1 <= y <= y2
            and
            y1 <= y <= y2
        )
    