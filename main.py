"""
main.py

GestureSurfer AI

Run this file and:

1. Camera starts immediately.
2. Subway Surfers launches automatically.
3. Subway Surfers goes fullscreen.
4. Camera becomes a small top-right overlay.
5. Game remains the keyboard target.
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
# CAMERA OVERLAY SETTINGS
# ============================================================

CAMERA_WINDOW = "GestureSurfer AI"

CAMERA_WIDTH = 360

CAMERA_HEIGHT = 240

CAMERA_MARGIN = 15


# ============================================================
# WINDOWS KEY HELPERS
# ============================================================

VK_F8 = 0x77

VK_Q = 0x51


def key_pressed(vk_code):

    return (
        ctypes.windll.user32.GetAsyncKeyState(
            vk_code
        )
        & 0x8000
    ) != 0


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

    x = (
        screen_width
        - CAMERA_WIDTH
        - CAMERA_MARGIN
    )

    y = CAMERA_MARGIN

    # Topmost
    HWND_TOPMOST = -1

    # Don't activate the camera window.
    SWP_NOACTIVATE = 0x0010

    SWP_SHOWWINDOW = 0x0040

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
    # INITIALIZE GAME LAUNCHER
    # ========================================================

    game_launcher = GameLauncher(
        GAME_URL
    )

    # ========================================================
    # INITIALIZE CAMERA FIRST
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

    game_controller = GameController()

    fps_counter = FPSCounter()

    # Controller starts ON.
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

    try:

        game_launcher.launch_game()

    except Exception as error:

        print(
            f"Game launch error: {error}"
        )

        print(
            "You can open Subway Surfers manually."
        )

    print()
    print("Camera is active.")
    print("Controller is ON.")
    print()
    print("Waiting for Subway Surfers...")

    # ========================================================
    # STATE
    # ========================================================

    camera_positioned = False

    game_focused = False

    last_game_focus = 0

    previous_f8 = False

    previous_q = False

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
                    .classify(
                        movement
                    )
                )

                # -------------------------------
                # FIST = HOVERBOARD
                # -------------------------------

                if (
                    fist_detector
                    .just_made_fist(
                        landmarks
                    )
                ):

                    action = ACTION_HOVERBOARD

                # -------------------------------
                # SEND GAME ACTION
                # -------------------------------

                if (
                    controller_enabled
                    and action != ACTION_NONE
                ):

                    success = (
                        game_controller
                        .execute(
                            action
                        )
                    )

                    if success:

                        print(
                            f"Action: {action}"
                        )

            else:

                gesture_classifier.reset()

                fist_detector.reset()

            # =================================================
            # FPS
            # =================================================

            fps = fps_counter.update()

            dx, dy = (
                motion_tracker.get_delta()
            )

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

            game_available = (
                game_launcher
                .is_game_available()
            )

            # -------------------------------------------------
            # Focus game only when it first appears.
            # -------------------------------------------------

            if (
                game_available
                and not game_focused
            ):

                time.sleep(0.2)

                if game_launcher.focus_game():

                    game_focused = True

                    print(
                        "Subway Surfers focused."
                    )

            # -------------------------------------------------
            # Reposition camera every 0.5 seconds.
            # -------------------------------------------------

            current_time = time.time()

            if (
                current_time
                - last_game_focus
                > 0.5
            ):

                position_camera()

                last_game_focus = (
                    current_time
                )

            # =================================================
            # GLOBAL F8
            # =================================================

            current_f8 = key_pressed(
                VK_F8
            )

            if (
                current_f8
                and not previous_f8
            ):

                controller_enabled = (
                    not controller_enabled
                )

                if controller_enabled:

                    game_controller.enable()

                    print(
                        "Controller ON"
                    )

                else:

                    game_controller.disable()

                    motion_tracker.reset()

                    fist_detector.reset()

                    print(
                        "Controller OFF"
                    )

            previous_f8 = current_f8

            # =================================================
            # GLOBAL Q
            # =================================================

            current_q = key_pressed(
                VK_Q
            )

            if (
                current_q
                and not previous_q
            ):

                print(
                    "Q pressed. Exiting..."
                )

                break

            previous_q = current_q

            # =================================================
            # PROCESS OPENCV
            # =================================================

            cv2.waitKey(1)

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