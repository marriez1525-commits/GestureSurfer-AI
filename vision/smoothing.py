"""
smoothing.py

Fast hand-position smoothing for GestureSurfer AI.

Uses a weighted average:
- Recent frames have more influence.
- Older frames have less influence.
- This reduces jitter without adding too much delay.
"""

from collections import deque


class MovementSmoother:

    def __init__(self, max_points=3):

        self.max_points = max_points

        self.x_history = deque(
            maxlen=max_points
        )

        self.y_history = deque(
            maxlen=max_points
        )

    def update(self, x, y):

        self.x_history.append(float(x))
        self.y_history.append(float(y))

    def get_smoothed_position(self):

        if not self.x_history:

            return None

        # -----------------------------------------
        # Weighted smoothing
        #
        # Most recent position gets the highest
        # weight.
        # -----------------------------------------

        count = len(self.x_history)

        weights = list(
            range(1, count + 1)
        )

        total_weight = sum(weights)

        weighted_x = sum(
            value * weight
            for value, weight in zip(
                self.x_history,
                weights
            )
        )

        weighted_y = sum(
            value * weight
            for value, weight in zip(
                self.y_history,
                weights
            )
        )

        average_x = (
            weighted_x / total_weight
        )

        average_y = (
            weighted_y / total_weight
        )

        return average_x, average_y

    def get_latest_position(self):

        if not self.x_history:

            return None

        return (
            self.x_history[-1],
            self.y_history[-1]
        )

    def reset(self):

        self.x_history.clear()
        self.y_history.clear()