"""
main.py

GestureSurfer AI

Features:
- Starts camera immediately
- Launches Subway Surfers automatically
- Maximizes Subway Surfers
- Places camera in top-right corner
- Keeps camera above the game
- Gestures control Subway Surfers
- Fist = Hoverboard
- Pinch = Continue
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
from vision.pinch_detector import PinchDetector

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
# WINDOWS CONSTANTS
# ============================================================

HWND_TOPMOST = -1

SWP_NOACTIVATE = 0x0010

SWP_SHOWWINDOW = 0x0040

SW_SHOWNOACTIVATE = 4


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

    # Top-right corner
    x = (
        screen_width
        - CAMERA_WIDTH
        - CAMERA_MARGIN
    )

    y = CAMERA_MARGIN

    # Show without activating
    user32.ShowWindow(
        hwnd,
        SW_SHOWNOACTIVATE
    )

    # Keep camera above other windows
    user32.SetWindowPos(
        hwnd,
        HWND_TOPMOST,
        x,
        y,
        CAMERA_WIDTH,
        CAMERA_HEIGHT,
        SWP_NOACTIVATE
        | SWP_SHOWWINDOW
    )

    return True


# ============================================================
# MAIN
# ============================================================

def main():

    # ========================================================
    # STARTUP
    # ========================================================

    print()
    print("=" * 60)
    print("                 GESTURESURFER AI")
    print("=" * 60)

    print()
    print("Starting camera first...")

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

    pinch_detector = PinchDetector()

    game_controller = GameController()

    fps_counter = FPSCounter()

    # ========================================================
    # CONTROLLER ON
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
    # LAUNCH GAME AFTER CAMERA IS READY
    # ========================================================

    game_launcher = GameLauncher(
        GAME_URL
    )

    try:

        game_launcher.launch_game()

    except Exception as error:

        print()
        print(
            f"Game launch error: {error}"
        )

        print(
            "Open Subway Surfers manually if needed."
        )

    # ========================================================
    # STATE
    # ========================================================

    camera_positioned = False

    game_found = False

    game_focus_done = False

    startup_time = time.time()

    # ========================================================
    # MAIN LOOP
    # ========================================================

    try:

        while True:

            # =================================================
            # CAMERA
            # =================================================

            frame = camera.read()

            if frame is None:

                continue

            # =================================================
            # HAND DETECTION
            # =================================================

            frame, landmarks = (
                detector.process(frame)
            )

            action = ACTION_NONE

            # =================================================
            # HAND FOUND
            # =================================================

            if landmarks is not None:

                # --------------------------------------------
                # Landmark tracker
                # --------------------------------------------

                landmark_tracker.update(
                    landmarks
                )

                # --------------------------------------------
                # Palm center
                # --------------------------------------------

                palm_position = (
                    landmark_tracker
                    .get_palm_center()
                )

                # --------------------------------------------
                # Movement
                # --------------------------------------------

                movement = (
                    motion_tracker.update(
                        palm_position
                    )
                )

                # --------------------------------------------
                # Gesture
                # --------------------------------------------

                action = (
                    gesture_classifier
                    .classify(
                        movement
                    )
                )

                # --------------------------------------------
                # FIST = HOVERBOARD
                # --------------------------------------------

                if (
                    fist_detector
                    .just_made_fist(
                        landmarks
                    )
                ):

                    action = ACTION_HOVERBOARD

                # --------------------------------------------
                # PINCH = CONTINUE
                # --------------------------------------------

                elif (
                    pinch_detector
                    .just_pinched(
                        landmarks
                    )
                ):

                    action = "CONTINUE"

                    if controller_enabled:

                        success = (
                            game_controller
                            .keyboard
                            .press("enter")
                        )

                        if success:

                            print(
                                "Action executed: CONTINUE"
                            )

                # --------------------------------------------
                # NORMAL GAME ACTION
                # --------------------------------------------

                if (
                    controller_enabled
                    and action != ACTION_NONE
                    and action != "CONTINUE"
                ):

                    success = (
                        game_controller
                        .execute(
                            action
                        )
                    )

                    if success:

                        print(
                            f"Action executed: {action}"
                        )

            # =================================================
            # HAND LOST
            # =================================================

            else:

                gesture_classifier.reset()

                fist_detector.reset()

                pinch_detector.reset()

            # =================================================
            # FPS
            # =================================================

            fps = fps_counter.update()

            dx, dy = (
                motion_tracker.get_delta()
            )

            # =================================================
            # UI
            # =================================================

            if detector.is_hand_detected():

                hand_text = "HAND: ON"
                hand_color = (0, 255, 0)

            else:

                hand_text = "HAND: LOST"
                hand_color = (0, 0, 255)

            cv2.putText(
                frame,
                f"FPS: {fps:.0f}",
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                hand_text,
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                hand_color,
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
                0.42,
                (255, 255, 255),
                1
            )

            cv2.putText(
                frame,
                "PINCH = CONTINUE",
                (10, 212),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.42,
                (255, 255, 255),
                1
            )

            # =================================================
            # SHOW CAMERA
            # =================================================

            cv2.imshow(
                CAMERA_WINDOW,
                frame
            )

            # =================================================
            # POSITION CAMERA
            # =================================================

            if not camera_positioned:

                camera_positioned = (
                    position_camera()
                )

            # =================================================
            # FIND GAME
            # =================================================

            if not game_found:

                game_found = (
                    game_launcher
                    .is_game_available()
                )

                if game_found:

                    print()
                    print(
                        "Subway Surfers detected."
                    )

            # =================================================
            # FOCUS GAME ONLY ONCE
            # =================================================

            if (
                game_found
                and not game_focus_done
            ):

                # Give game a moment to finish
                # loading its window.

                time.sleep(0.5)

                if game_launcher.focus_game():

                    game_focus_done = True

                    print(
                        "Subway Surfers focused."
                    )

            # =================================================
            # KEEP CAMERA TOPMOST
            # =================================================

            position_camera()

            # =================================================
            # Q
            # =================================================

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):

                print()
                print(
                    "Q pressed. Exiting..."
                )

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


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()