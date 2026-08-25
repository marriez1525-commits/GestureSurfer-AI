"""
main.py

GestureSurfer AI

Starts:
    Subway Surfers
    Camera overlay
    Gesture controller

The camera appears in the top-right corner.
"""

import ctypes
import time

import cv2

from camera.camera import Camera
from camera.fps import FPSCounter

from vision.hand_detector import HandDetector
from vision.landmark_tracker import LandmarkTracker
from vision.motion_tracker import MotionTracker
from vision.gesture_classifier import GestureClassifier
from vision.fist_detector import FistDetector

from controller.game_controller import GameController

from launcher.game_launcher import GameLauncher

from config import (
    ACTION_NONE,
    ACTION_HOVERBOARD,
    GAME_URL,
)


# ============================================================
# CAMERA WINDOW
# ============================================================

CAMERA_WINDOW = "GestureSurfer AI"

CAMERA_WIDTH = 360

CAMERA_HEIGHT = 240

CAMERA_MARGIN = 15


# ============================================================
# POSITION CAMERA
# ============================================================

def position_camera():

    user32 = ctypes.windll.user32

    hwnd = user32.FindWindowW(
        None,
        CAMERA_WINDOW
    )

    if not hwnd:

        return False

    screen_width = (
        user32.GetSystemMetrics(0)
    )

    # Top-right position
    x = (
        screen_width
        - CAMERA_WIDTH
        - CAMERA_MARGIN
    )

    y = CAMERA_MARGIN

    # Windows constants
    HWND_TOPMOST = -1

    SWP_NOACTIVATE = 0x0010

    SWP_SHOWWINDOW = 0x0040

    flags = (
        SWP_NOACTIVATE
        | SWP_SHOWWINDOW
    )

    user32.SetWindowPos(
        hwnd,
        HWND_TOPMOST,
        x,
        y,
        CAMERA_WIDTH,
        CAMERA_HEIGHT,
        flags
    )

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    # ========================================================
    # LAUNCH GAME
    # ========================================================

    game_launcher = GameLauncher(
        GAME_URL
    )

    try:

        game_launcher.launch_game()

    except Exception as error:

        print(
            f"Game launch error: {error}"
        )

        print(
            "Open Subway Surfers manually."
        )

    # ========================================================
    # CAMERA
    # ========================================================

    camera = Camera()

    detector = HandDetector()

    landmark_tracker = LandmarkTracker()

    motion_tracker = MotionTracker()

    gesture_classifier = (
        GestureClassifier()
    )

    fist_detector = FistDetector()

    game_controller = GameController()

    fps_counter = FPSCounter()

    # ========================================================
    # CONTROLLER ALWAYS ON
    # ========================================================

    controller_enabled = True

    game_controller.enable()

    # ========================================================
    # CAMERA WINDOW
    # ========================================================

    cv2.namedWindow(
        CAMERA_WINDOW,
        cv2.WINDOW_NORMAL
    )

    cv2.resizeWindow(
        CAMERA_WINDOW,
        CAMERA_WIDTH,
        CAMERA_HEIGHT
    )

    # ========================================================
    # START
    # ========================================================

    print()
    print("=" * 55)
    print("            GESTURESURFER AI")
    print("=" * 55)

    print()
    print("LEFT  = move left")
    print("RIGHT = move right")
    print("UP    = jump")
    print("DOWN  = roll")
    print("FIST  = hoverboard")

    print()
    print("Controller: ON")

    print()
    print("Camera starting...")

    time.sleep(2)

    # ========================================================
    # STATE
    # ========================================================

    camera_positioned = False

    game_focused = False

    frame_count = 0

    # ========================================================
    # MAIN LOOP
    # ========================================================

    try:

        while True:

            # ------------------------------------------------
            # CAMERA READ
            # ------------------------------------------------

            frame = camera.read()

            if frame is None:

                print(
                    "Camera frame unavailable."
                )

                break

            # ------------------------------------------------
            # HAND
            # ------------------------------------------------

            frame, landmarks = (
                detector.process(frame)
            )

            action = ACTION_NONE

            # ------------------------------------------------
            # HAND FOUND
            # ------------------------------------------------

            if landmarks is not None:

                landmark_tracker.update(
                    landmarks
                )

                palm_position = (
                    landmark_tracker
                    .get_palm_center()
                )

                movement = (
                    motion_tracker.update(
                        palm_position
                    )
                )

                action = (
                    gesture_classifier
                    .classify(movement)
                )

                # FIST
                if (
                    fist_detector
                    .just_made_fist(
                        landmarks
                    )
                ):

                    action = ACTION_HOVERBOARD

                # SEND GAME ACTION
                if (
                    controller_enabled
                    and action != ACTION_NONE
                ):

                    success = (
                        game_controller
                        .execute(action)
                    )

                    if success:

                        print(
                            f"Action: {action}"
                        )

            else:

                gesture_classifier.reset()

                fist_detector.reset()

                # Reset tracker only after a genuine
                # hand loss.
                motion_tracker.reset()

            # ------------------------------------------------
            # DEBUG DATA
            # ------------------------------------------------

            fps = fps_counter.update()

            dx, dy = (
                motion_tracker.get_delta()
            )

            # ------------------------------------------------
            # DRAW
            # ------------------------------------------------

            cv2.putText(
                frame,
                f"FPS: {fps:.0f}",
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2
            )

            if detector.is_hand_detected():

                cv2.putText(
                    frame,
                    "HAND: ON",
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 255, 0),
                    2
                )

            else:

                cv2.putText(
                    frame,
                    "HAND: LOST",
                    (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 0, 255),
                    2
                )

            cv2.putText(
                frame,
                f"DX: {dx:.3f}",
                (10, 78),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 255, 255),
                1
            )

            cv2.putText(
                frame,
                f"DY: {dy:.3f}",
                (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 255, 255),
                1
            )

            cv2.putText(
                frame,
                f"ACTION: {action}",
                (10, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.60,
                (255, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "CONTROLLER ON",
                (10, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.50,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "FIST = HOVERBOARD",
                (10, 190),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.43,
                (255, 255, 255),
                1
            )

            # ------------------------------------------------
            # SHOW
            # ------------------------------------------------

            cv2.imshow(
                CAMERA_WINDOW,
                frame
            )

            # ------------------------------------------------
            # CAMERA OVERLAY
            # ------------------------------------------------

            if not camera_positioned:

                cv2.waitKey(1)

                camera_positioned = (
                    position_camera()
                )

            # ------------------------------------------------
            # FOCUS GAME ONLY ONCE
            # ------------------------------------------------

            if (
                camera_positioned
                and not game_focused
            ):

                time.sleep(0.2)

                game_focused = (
                    game_launcher
                    .focus_game()
                )

            # ------------------------------------------------
            # REPOSITION PERIODICALLY
            # ------------------------------------------------

            frame_count += 1

            if frame_count >= 120:

                frame_count = 0

                position_camera()

                # Keep game focused
                game_launcher.focus_game()

            # ------------------------------------------------
            # OpenCV keyboard
            # ------------------------------------------------

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):

                break

    except KeyboardInterrupt:

        pass

    finally:

        print()
        print(
            "Stopping GestureSurfer AI..."
        )

        game_controller.stop()

        detector.close()

        camera.release()

        cv2.destroyAllWindows()

        game_launcher.close_game()

        print(
            "GestureSurfer AI stopped safely."
        )


if __name__ == "__main__":

    main()