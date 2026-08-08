"""
test_controller.py

Tests the GestureSurfer keyboard controller
without using the webcam or Subway Surfers.
"""

import time

from controller.game_controller import GameController

from config import (
    ACTION_LEFT,
    ACTION_RIGHT,
    ACTION_JUMP,
    ACTION_ROLL,
)


def main():

    controller = GameController()

    print("=" * 45)
    print("       GESTURESURFER AI")
    print("       CONTROLLER TEST")
    print("=" * 45)

    print()
    print("The controller will test:")
    print()
    print("LEFT  -> Left Arrow")
    print("RIGHT -> Right Arrow")
    print("JUMP  -> Up Arrow")
    print("ROLL  -> Down Arrow")
    print()

    print("IMPORTANT:")
    print("Click inside a text editor before the test starts.")
    print("The program will send real keyboard presses.")
    print()

    input("Press ENTER when you are ready...")

    print()
    print("Starting in 3 seconds...")

    time.sleep(3)

    # --------------------------------------------------
    # LEFT
    # --------------------------------------------------

    print("Testing LEFT...")

    controller.execute(ACTION_LEFT)

    time.sleep(1)

    # --------------------------------------------------
    # RIGHT
    # --------------------------------------------------

    print("Testing RIGHT...")

    controller.execute(ACTION_RIGHT)

    time.sleep(1)

    # --------------------------------------------------
    # JUMP
    # --------------------------------------------------

    print("Testing JUMP...")

    controller.execute(ACTION_JUMP)

    time.sleep(1)

    # --------------------------------------------------
    # ROLL
    # --------------------------------------------------

    print("Testing ROLL...")

    controller.execute(ACTION_ROLL)

    time.sleep(1)

    # --------------------------------------------------
    # Finish
    # --------------------------------------------------

    controller.stop()

    print()
    print("=" * 45)
    print("CONTROLLER TEST COMPLETE")
    print("=" * 45)


if __name__ == "__main__":
    main()