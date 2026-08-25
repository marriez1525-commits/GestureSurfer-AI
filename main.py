"""
main.py

GestureSurfer AI

Features:
- Automatically launches Subway Surfers
- Automatically starts webcam
- Camera appears as a top-right overlay
- Camera stays above the game
- Game remains the keyboard target
- LEFT / RIGHT / JUMP / ROLL gestures
- Fist = Hoverboard
- Pinch = Continue / Resume
- Q = Quit
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
# CAMERA WINDOW SETTINGS
# ============================================================

CAMERA_WINDOW = "GestureSurfer AI"

CAMERA_WIDTH = 360

CAMERA_HEIGHT = 240

CAMERA_MARGIN = 15


# ============================================================
# WINDOWS KEY CODES
# ============================================================

VK_Q = 0x51


# ============================================================
# POSITION CAMERA OVERLAY
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

    screen_height = (
        user32.GetSystemMetrics(1)
    )

    # -----------------------------------------------
    # Top-right corner
    # -----------------------------------------------

    x = (
        screen_width
        - CAMERA_WIDTH
        - CAMERA_MARGIN
    )

    y = CAMERA_MARGIN

    # -----------------------------------------------
    # Windows constants
    # -----------------------------------------------

    HWND_TOPMOST = -1

    SWP_NOACTIVATE = 0x0010

    SWP_SHOWWINDOW = 0x0040

    # -----------------------------------------------
    # Put camera above game without activating it
    # -----------------------------------------------

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
    # START GAME LAUNCHER
    # ========================================================

    game_launcher = GameLauncher(
        GAME_URL
    )

    # ========================================================
    # START CAMERA FIRST
    # ========================================================

    print()
    print("=" * 60)
    print("                 GESTURESURFER AI")
    print("=" * 60)

    print()
    print("Starting camera...")

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
    # CONTROLLER STARTS ON
    # ========================================================

    controller_enabled = True

    game_controller.enable()

    # ========================================================
    # CREATE CAMERA WINDOW
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
    # LAUNCH SUBWAY SURFERS
    # ========================================================

    try:

        game_launcher.launch_game()

    except Exception as error:

        print()
        print(
            f"Game launch error: {error}"
        )

        print(
            "You can open Subway Surfers manually."
        )

    # ========================================================
    # STARTUP MESSAGE
    # ========================================================

    print()
    print("Camera is active.")
    print("Controller is ON.")
    print()
    print("Controls:")
    print("  LEFT   -> Left")
    print("  RIGHT  -> Right")
    print("  UP     -> Jump")
    print("  DOWN   -> Roll")
    print("  FIST   -> Hoverboard")
    print("  PINCH  -> Continue")
    print("  Q      -> Quit")
    print()

    # ========================================================
    # STATE
    # ========================================================

    camera_positioned = False

    game_focused = False

    last_camera_position_time = 0

    last_game_focus_time = 0

    # ========================================================
    # MAIN LOOP
    # ========================================================

    try:

        while True:

            # =================================================
            # READ CAMERA
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
                # Normal movement action
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

                    # Send Enter directly.
                    #
                    # We don't send it through the normal
                    # movement mapping.
                    if controller_enabled:

                        success = (
                            game_controller.keyboard
                            .press("enter")
                        )

                        if success:

                            print(
                                "Action executed: CONTINUE"
                            )

                    action = "CONTINUE"

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
            # HAND NOT FOUND
            # =================================================

            else:

                gesture_classifier.reset()

                fist_detector.reset()

                pinch_detector.reset()

            # =================================================
            # FPS
            # =================================================

            fps = fps_counter.update()

            # =================================================
            # MOVEMENT DEBUG
            # =================================================

            delta_x, delta_y = (
                motion_tracker.get_delta()
            )

            # =================================================
            # HAND STATUS
            # =================================================

            if detector.is_hand_detected():

                hand_text = "HAND: ON"

            else:

                hand_text = "HAND: LOST"

            # =================================================
            # CAMERA UI
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

            cv2.putText(
                frame,
                hand_text,
                (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0)
                if detector.is_hand_detected()
                else (0, 0, 255),
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

            current_time = time.time()

            if (
                not camera_positioned
                or
                current_time
                - last_camera_position_time
                > 0.5
            ):

                if position_camera():

                    camera_positioned = True

                last_camera_position_time = (
                    current_time
                )

            # =================================================
            # KEEP GAME FOCUSED
            # =================================================

            if (
                not game_focused
                or
                current_time
                - last_game_focus_time
                > 2.0
            ):

                if game_launcher.focus_game():

                    game_focused = True

                last_game_focus_time = (
                    current_time
                )

            # =================================================
            # OPENCV EVENT PROCESSING
            # =================================================

            cv2.waitKey(1)

            # =================================================
            # GLOBAL Q
            # =================================================

            if (
                ctypes.windll.user32
                .GetAsyncKeyState(VK_Q)
                & 0x8000
            ):

                print()
                print(
                    "Q pressed. Exiting..."
                )

                break

    except KeyboardInterrupt:

        print()
        print(
            "Program interrupted."
        )

    finally:

        # =====================================================
        # CLEANUP
        # =====================================================

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