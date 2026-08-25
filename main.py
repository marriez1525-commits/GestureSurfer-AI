"""
main.py

GestureSurfer AI

Features:
- Automatically launches Subway Surfers
- Automatically opens webcam
- Camera appears in top-right corner
- Camera stays above the game
- Hand gestures control the game
- Fist activates hoverboard
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
# WINDOWS HELPER
# ============================================================

def position_camera_window():

    user32 = ctypes.windll.user32

    # Find OpenCV camera window
    hwnd = user32.FindWindowW(
        None,
        CAMERA_WINDOW
    )

    if not hwnd:
        return False

    # Screen dimensions
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    # Top-right corner
    x = (
        screen_width
        - CAMERA_WIDTH
        - CAMERA_MARGIN
    )

    y = CAMERA_MARGIN

    # HWND_TOPMOST
    HWND_TOPMOST = -1

    # Flags
    SWP_SHOWWINDOW = 0x0040

    user32.SetWindowPos(
        hwnd,
        HWND_TOPMOST,
        x,
        y,
        CAMERA_WIDTH,
        CAMERA_HEIGHT,
        SWP_SHOWWINDOW
    )

    # Show window
    user32.ShowWindow(
        hwnd,
        5
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
            f"Could not launch Subway Surfers: {error}"
        )

        print(
            "You can open the game manually."
        )

    # ========================================================
    # INITIALIZE CAMERA
    # ========================================================

    camera = Camera()

    detector = HandDetector()

    landmark_tracker = LandmarkTracker()

    motion_tracker = MotionTracker()

    gesture_classifier = GestureClassifier()

    fist_detector = FistDetector()

    game_controller = GameController()

    fps_counter = FPSCounter()

    # ========================================================
    # CONTROLLER STARTS ON
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
    # STARTUP
    # ========================================================

    print()
    print("=" * 60)
    print("                 GESTURESURFER AI")
    print("=" * 60)

    print()
    print("LEFT  -> Move left")
    print("RIGHT -> Move right")
    print("UP    -> Jump")
    print("DOWN  -> Roll")
    print("FIST  -> Hoverboard")

    print()
    print("F8 -> Controller ON/OFF")
    print("Q  -> Quit")

    print()
    print("Controller is ON.")

    print()
    print("Starting camera...")

    # ========================================================
    # MAIN LOOP
    # ========================================================

    camera_positioned = False

    frame_counter = 0

    try:

        while True:

            # ------------------------------------------------
            # READ CAMERA
            # ------------------------------------------------

            frame = camera.read()

            if frame is None:

                print(
                    "Could not read camera frame."
                )

                break

            # ------------------------------------------------
            # HAND DETECTION
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
                    landmark_tracker.get_palm_center()
                )

                movement = (
                    motion_tracker.update(
                        palm_position
                    )
                )

                action = (
                    gesture_classifier.classify(
                        movement
                    )
                )

                # FIST = HOVERBOARD
                if fist_detector.just_made_fist(
                    landmarks
                ):

                    action = ACTION_HOVERBOARD

                # Send game action
                if (
                    controller_enabled
                    and action != ACTION_NONE
                ):

                    success = (
                        game_controller.execute(
                            action
                        )
                    )

                    if success:

                        print(
                            f"Action executed: {action}"
                        )

            else:

                gesture_classifier.reset()

                fist_detector.reset()

            # ------------------------------------------------
            # FPS
            # ------------------------------------------------

            fps = fps_counter.update()

            # ------------------------------------------------
            # MOVEMENT
            # ------------------------------------------------

            delta_x, delta_y = (
                motion_tracker.get_delta()
            )

            # =================================================
            # DRAW CAMERA UI
            # =================================================

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
                f"DX: {delta_x:.3f}",
                (10, 78),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (255, 255, 255),
                1
            )

            cv2.putText(
                frame,
                f"DY: {delta_y:.3f}",
                (10, 101),
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
                0.6,
                (255, 255, 0),
                2
            )

            if controller_enabled:

                cv2.putText(
                    frame,
                    "CONTROLLER ON",
                    (10, 160),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

            else:

                cv2.putText(
                    frame,
                    "CONTROLLER OFF",
                    (10, 160),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    2
                )

            cv2.putText(
                frame,
                "FIST = HOVERBOARD",
                (10, 190),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.42,
                (255, 255, 255),
                1
            )

            cv2.putText(
                frame,
                "F8 = ON/OFF | Q = QUIT",
                (10, 215),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.40,
                (255, 255, 255),
                1
            )

            # ------------------------------------------------
            # SHOW CAMERA
            # ------------------------------------------------

            cv2.imshow(
                CAMERA_WINDOW,
                frame
            )

            # ------------------------------------------------
            # POSITION CAMERA
            # ------------------------------------------------

            if not camera_positioned:

                cv2.waitKey(1)

                # Try several times during startup.
                if position_camera_window():

                    camera_positioned = True

                    print(
                        "Camera positioned top-right."
                    )

            # ------------------------------------------------
            # Re-assert camera position occasionally.
            #
            # This helps if Chrome temporarily covers it.
            # ------------------------------------------------

            frame_counter += 1

            if frame_counter >= 60:

                frame_counter = 0

                position_camera_window()

            # ------------------------------------------------
            # KEY INPUT
            # ------------------------------------------------

            key = cv2.waitKey(1) & 0xFF

            # F8
            if key == 0x77:

                controller_enabled = (
                    not controller_enabled
                )

                if controller_enabled:

                    game_controller.enable()

                    print(
                        "Controller enabled."
                    )

                else:

                    game_controller.disable()

                    motion_tracker.reset()

                    fist_detector.reset()

                    print(
                        "Controller disabled."
                    )

            # Q
            elif key == ord("q"):

                print(
                    "Q pressed. Exiting..."
                )

                break

    except KeyboardInterrupt:

        print(
            "Program interrupted."
        )

    finally:

        print(
            "Stopping GestureSurfer AI..."
        )

        game_controller.stop()

        fist_detector.reset()

        detector.close()

        camera.release()

        cv2.destroyAllWindows()

        game_launcher.close_game()

        print(
            "GestureSurfer AI stopped safely."
        )


if __name__ == "__main__":

    main()