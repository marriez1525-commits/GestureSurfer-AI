"""
main.py

GestureSurfer AI

Features:
- Launches Subway Surfers automatically
- Opens webcam automatically
- Hand gesture control
- LEFT / RIGHT / JUMP / ROLL
- Fist = Hoverboard
- Camera overlay can be placed on top of the game

Controls:
    F8 = Controller ON/OFF
    Q  = Quit
"""

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
    CAMERA_WINDOW_WIDTH,
    CAMERA_WINDOW_HEIGHT,
)


# ============================================================
# WINDOW NAME
# ============================================================

CAMERA_WINDOW = "GestureSurfer AI"


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
    # LAUNCH SUBWAY SURFERS
    # ========================================================

    try:

        game_launcher.launch_game()

    except Exception as error:

        print()
        print(
            f"Could not automatically launch Subway Surfers: "
            f"{error}"
        )

        print()
        print(
            "The camera controller will still start."
        )

    # ========================================================
    # INITIALIZE CAMERA
    # ========================================================

    camera = Camera()

    # ========================================================
    # INITIALIZE COMPUTER VISION
    # ========================================================

    detector = HandDetector()

    landmark_tracker = LandmarkTracker()

    motion_tracker = MotionTracker()

    gesture_classifier = GestureClassifier()

    fist_detector = FistDetector()

    # ========================================================
    # INITIALIZE GAME CONTROLLER
    # ========================================================

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
        CAMERA_WINDOW_WIDTH,
        CAMERA_WINDOW_HEIGHT
    )

    # ========================================================
    # STARTUP
    # ========================================================

    print()
    print("=" * 60)
    print("                 GESTURESURFER AI")
    print("=" * 60)

    print()
    print("Hand Controls:")
    print("    LEFT  -> Left Arrow")
    print("    RIGHT -> Right Arrow")
    print("    UP    -> Jump")
    print("    DOWN  -> Roll")
    print("    FIST  -> Hoverboard")

    print()
    print("Keyboard Controls:")
    print("    F8 -> Controller ON/OFF")
    print("    Q  -> Quit")

    print()
    print("Controller: ON")

    print()
    print("Starting camera in 3 seconds...")

    time.sleep(3)

    print()
    print("Camera started.")
    print("GestureSurfer AI is ready.")
    print()

    # ========================================================
    # CAMERA POSITIONING STATE
    # ========================================================

    camera_positioned = False

    # ========================================================
    # MAIN LOOP
    # ========================================================

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

                # --------------------------------------------
                # Update landmark tracker
                # --------------------------------------------

                landmark_tracker.update(
                    landmarks
                )

                # --------------------------------------------
                # Get palm position
                # --------------------------------------------

                palm_position = (
                    landmark_tracker.get_palm_center()
                )

                # --------------------------------------------
                # Motion detection
                # --------------------------------------------

                movement = (
                    motion_tracker.update(
                        palm_position
                    )
                )

                # --------------------------------------------
                # Gesture classification
                # --------------------------------------------

                action = (
                    gesture_classifier.classify(
                        movement
                    )
                )

                # --------------------------------------------
                # FIST = HOVERBOARD
                # --------------------------------------------

                if fist_detector.just_made_fist(
                    landmarks
                ):

                    action = ACTION_HOVERBOARD

                # --------------------------------------------
                # SEND ACTION
                # --------------------------------------------

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

            # ------------------------------------------------
            # HAND NOT FOUND
            # ------------------------------------------------

            else:

                gesture_classifier.reset()

                fist_detector.reset()

            # =================================================
            # FPS
            # =================================================

            fps = fps_counter.update()

            # =================================================
            # MOVEMENT VALUES
            # =================================================

            delta_x, delta_y = (
                motion_tracker.get_delta()
            )

            # =================================================
            # DRAW FPS
            # =================================================

            cv2.putText(
                frame,
                f"FPS: {fps:.1f}",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 255, 0),
                2
            )

            # =================================================
            # HAND STATUS
            # =================================================

            if detector.is_hand_detected():

                cv2.putText(
                    frame,
                    "HAND: DETECTED",
                    (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 255, 0),
                    2
                )

            else:

                cv2.putText(
                    frame,
                    "HAND: NOT DETECTED",
                    (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 0, 255),
                    2
                )

            # =================================================
            # DX
            # =================================================

            cv2.putText(
                frame,
                f"DX: {delta_x:.3f}",
                (20, 95),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

            # =================================================
            # DY
            # =================================================

            cv2.putText(
                frame,
                f"DY: {delta_y:.3f}",
                (20, 125),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (255, 255, 255),
                2
            )

            # =================================================
            # ACTION
            # =================================================

            cv2.putText(
                frame,
                f"ACTION: {action}",
                (20, 165),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (255, 255, 0),
                2
            )

            # =================================================
            # CONTROLLER
            # =================================================

            if controller_enabled:

                cv2.putText(
                    frame,
                    "CONTROLLER: ON",
                    (20, 200),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 255, 0),
                    2
                )

            else:

                cv2.putText(
                    frame,
                    "CONTROLLER: OFF",
                    (20, 200),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (0, 0, 255),
                    2
                )

            # =================================================
            # INSTRUCTIONS
            # =================================================

            cv2.putText(
                frame,
                "F8 = ON/OFF",
                (20, 230),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )

            cv2.putText(
                frame,
                "FIST = HOVERBOARD",
                (20, 255),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1
            )

            cv2.putText(
                frame,
                "Q = QUIT",
                (20, 280),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
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
            # POSITION CAMERA OVERLAY
            # =================================================

            if not camera_positioned:

                # Give OpenCV a moment to create window.
                cv2.waitKey(1)

                positioned = (
                    game_launcher.make_camera_topmost(
                        CAMERA_WINDOW
                    )
                )

                if positioned:

                    camera_positioned = True

                    # Return focus to game.
                    game_launcher.focus_game()

            # =================================================
            # KEYBOARD INPUT
            # =================================================

            key = (
                cv2.waitKey(1)
                & 0xFF
            )

            # ------------------------------------------------
            # F8 = CONTROLLER ON/OFF
            # ------------------------------------------------

            if key == 0x77:

                controller_enabled = (
                    not controller_enabled
                )

                if controller_enabled:

                    game_controller.enable()

                    print()
                    print(
                        "CONTROLLER ENABLED"
                    )

                else:

                    game_controller.disable()

                    motion_tracker.reset()

                    fist_detector.reset()

                    print()
                    print(
                        "CONTROLLER DISABLED"
                    )

            # ------------------------------------------------
            # Q = QUIT
            # ------------------------------------------------

            elif key == ord("q"):

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
            "Stopping controller..."
        )

        game_controller.stop()

        fist_detector.reset()

        detector.close()

        camera.release()

        cv2.destroyAllWindows()

        # Close automatically launched game
        game_launcher.close_game()

        print(
            "GestureSurfer AI stopped safely."
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()