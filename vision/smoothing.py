"""
smoothing.py

Fast weighted smoothing for gameplay.
"""

from collections import deque


class MovementSmoother:

    def __init__(self, max_points=2):

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

        count = len(
            self.x_history
        )

        weights = list(
            range(1, count + 1)
        )

        total_weight = sum(weights)

        weighted_x = sum(
            x * w
            for x, w in zip(
                self.x_history,
                weights
            )
        )

        weighted_y = sum(
            y * w
            for y, w in zip(
                self.y_history,
                weights
            )
        )

        return (
            weighted_x / total_weight,
            weighted_y / total_weight
        )

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