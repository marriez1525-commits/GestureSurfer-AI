"""
landmark_tracker.py

Provides easy access to important hand landmark positions
detected by MediaPipe.
"""

import math


class LandmarkTracker:
    """
    Extracts useful coordinates from MediaPipe hand landmarks.
    """

    # MediaPipe landmark indexes
    WRIST = 0

    THUMB_TIP = 4

    INDEX_TIP = 8
    INDEX_PIP = 6

    MIDDLE_TIP = 12
    MIDDLE_PIP = 10

    RING_TIP = 16
    RING_PIP = 14

    PINKY_TIP = 20
    PINKY_PIP = 18

    def __init__(self):
        self.landmarks = None

    def update(self, landmarks):
        """
        Update the current hand landmarks.
        """

        self.landmarks = landmarks

    def get_point(self, landmark_id):
        """
        Return the x and y coordinates of a landmark.

        MediaPipe coordinates are normalized between 0 and 1.
        """

        if self.landmarks is None:
            return None

        if landmark_id >= len(self.landmarks):
            return None

        landmark = self.landmarks[landmark_id]

        return landmark.x, landmark.y

    def get_wrist(self):
        """
        Return the wrist coordinates.
        """

        return self.get_point(self.WRIST)

    def get_index_tip(self):
        """
        Return the index fingertip coordinates.
        """

        return self.get_point(self.INDEX_TIP)

    def get_middle_tip(self):
        """
        Return the middle fingertip coordinates.
        """

        return self.get_point(self.MIDDLE_TIP)

    def get_palm_center(self):
        """
        Calculate a stable center position for the palm.

        Uses several palm landmarks instead of one finger,
        so movement works with different hand poses:

            Open hand
            One finger
            Two fingers
            Fist
        """

        if self.landmarks is None:
            return None

        # Important palm landmarks
        palm_ids = [
            0,   # Wrist
            5,   # Index MCP
            9,   # Middle MCP
            13,  # Ring MCP
            17   # Pinky MCP
        ]

        points = []

        for landmark_id in palm_ids:

            point = self.landmarks[landmark_id]

            points.append(point)

        # Calculate average X coordinate
        average_x = sum(
            point.x for point in points
        ) / len(points)

        # Calculate average Y coordinate
        average_y = sum(
            point.y for point in points
        ) / len(points)

        return average_x, average_y

    def distance(self, point1, point2):
        """
        Calculate the distance between two points.
        """

        if point1 is None or point2 is None:
            return 0

        x_difference = point1[0] - point2[0]

        y_difference = point1[1] - point2[1]

        return math.sqrt(
            x_difference ** 2 +
            y_difference ** 2
        )

    def is_finger_extended(self, tip_id, pip_id):
        """
        Determine whether a finger is extended.

        This is currently used for future gesture
        recognition features.
        """

        tip = self.get_point(tip_id)

        pip = self.get_point(pip_id)

        if tip is None or pip is None:
            return False

        return tip[1] < pip[1]

    def get_finger_states(self):
        """
        Return the state of the four non-thumb fingers.

        Returns:
            Dictionary containing True/False values.
        """

        if self.landmarks is None:
            return {
                "index": False,
                "middle": False,
                "ring": False,
                "pinky": False
            }

        return {
            "index": self.is_finger_extended(
                self.INDEX_TIP,
                self.INDEX_PIP
            ),

            "middle": self.is_finger_extended(
                self.MIDDLE_TIP,
                self.MIDDLE_PIP
            ),

            "ring": self.is_finger_extended(
                self.RING_TIP,
                self.RING_PIP
            ),

            "pinky": self.is_finger_extended(
                self.PINKY_TIP,
                self.PINKY_PIP
            )
        }