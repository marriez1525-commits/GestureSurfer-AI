"""
main.py

GestureSurfer AI

Combines:
Webcam
MediaPipe hand tracking
Palm movement detection
Gesture classification
Fist detection
Keyboard controller

Controls:
F8    = Controller ON/OFF
Q     = Quit

Hand gestures:
Swipe LEFT  = Left Arrow
Swipe RIGHT = Right Arrow
Swipe UP    = Jump
Swipe DOWN  = Roll
Fist        = Hoverboard / Space
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

from config import (
    ACTION_NONE,
    ACTION_HOVERBOARD,
)


def main():

    # ======================================================
    # INITIALIZE
    # ======================================================

    camera = Camera()

    detector = HandDetector()

    landmark_tracker = LandmarkTracker()

    motion_tracker = MotionTracker()

    gesture_classifier = GestureClassifier()

    fist_detector = FistDetector()

    game_controller = GameController()

    fps_counter = FPSCounter()

    # ======================================================
    # CONTROLLER STARTS ON
    # ======================================================

    controller_enabled = True

    game_controller.enable()

    # ======================================================
    # STARTUP
    # ======================================================

    print("=" * 60)
    print("                 GESTURESURFER AI")
    print("=" * 60)

    print()

    print("Hand Controls:")
    print("    Move LEFT  -> Left Arrow")
    print("    Move RIGHT -> Right Arrow")
    print("    Move UP    -> Up Arrow")
    print("    Move DOWN  -> Down Arrow")
    print("    FIST       -> Hoverboard / Space")

    print()

    print("Keyboard Controls:")
    print("    F8 -> Controller ON/OFF")
    print("    Q  -> Quit")

    print()

    print("The controller is currently ON.")

    print()

    print("Starting camera in 3 seconds...")

    time.sleep(3)

    print()

    print("Camera started.")
    print("Show your hand to the camera.")

    print()

    # ======================================================
    # MAIN LOOP
    # ======================================================

    try:

        while True:

            # ------------------------------------------------
            # CAMERA
            # ------------------------------------------------

            frame = camera.read()

            if frame is None:

                print("Could not read camera frame.")

                break

            # ------------------------------------------------
            # HAND DETECTION
            # ------------------------------------------------

            frame, landmarks = detector.process(frame)

            # Default action

            action = ACTION_NONE

            # ------------------------------------------------
            # HAND FOUND
            # ------------------------------------------------

            if landmarks is not None:

                # --------------------------------------------
                # Update landmark tracker
                # --------------------------------------------

                landmark_tracker.update(landmarks)

                # --------------------------------------------
                # Get palm position
                # --------------------------------------------

                palm_position = (
                    landmark_tracker.get_palm_center()
                )

                # --------------------------------------------
                # Detect movement
                # --------------------------------------------

                movement = motion_tracker.update(
                    palm_position
                )

                # --------------------------------------------
                # Convert movement into action
                # --------------------------------------------

                action = gesture_classifier.classify(
                    movement
                )

                # --------------------------------------------
                # FIST = HOVERBOARD
                # --------------------------------------------

                if fist_detector.just_made_fist(
                    landmarks
                ):

                    action = ACTION_HOVERBOARD

                # --------------------------------------------
                # SEND KEYBOARD ACTION
                # --------------------------------------------

                if (
                    controller_enabled
                    and action != ACTION_NONE
                ):

                    success = game_controller.execute(
                        action
                    )

                    # Debug information
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

            # ==================================================
            # FPS
            # ==================================================

            fps = fps_counter.update()

            # ==================================================
            # MOVEMENT VALUES
            # ==================================================

            delta_x, delta_y = (
                motion_tracker.get_delta()
            )

            # ==================================================
            # DISPLAY FPS
            # ==================================================

            cv2.putText(
                frame,
                f"FPS: {fps:.1f}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            # ==================================================
            # HAND STATUS
            # ==================================================

            if detector.is_hand_detected():

                cv2.putText(
                    frame,
                    "HAND: DETECTED",
                    (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

            else:

                cv2.putText(
                    frame,
                    "HAND: NOT DETECTED",
                    (20, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

            # ==================================================
            # DX
            # ==================================================

            cv2.putText(
                frame,
                f"DX: {delta_x:.3f}",
                (20, 110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            # ==================================================
            # DY
            # ==================================================

            cv2.putText(
                frame,
                f"DY: {delta_y:.3f}",
                (20, 140),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            # ==================================================
            # ACTION
            # ==================================================

            cv2.putText(
                frame,
                f"ACTION: {action}",
                (20, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 0),
                2
            )

            # ==================================================
            # CONTROLLER STATUS
            # ==================================================

            if controller_enabled:

                cv2.putText(
                    frame,
                    "CONTROLLER: ON",
                    (20, 220),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            else:

                cv2.putText(
                    frame,
                    "CONTROLLER: OFF",
                    (20, 220),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

            # ==================================================
            # INSTRUCTIONS
            # ==================================================

            cv2.putText(
                frame,
                "F8 = ON/OFF",
                (20, 260),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "FIST = HOVERBOARD",
                (20, 290),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                "Q = QUIT",
                (20, 320),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

            # ==================================================
            # SHOW CAMERA
            # ==================================================

            cv2.imshow(
                "GestureSurfer AI",
                frame
            )

            # ==================================================
            # KEYBOARD INPUT
            # ==================================================

            key = cv2.waitKey(1) & 0xFF

            # ------------------------------------------------
            # F8 = TOGGLE CONTROLLER
            #
            # IMPORTANT:
            # We no longer use SPACE here.
            # SPACE is reserved for Subway Surfers.
            # ------------------------------------------------

            if key == 0x77:

                controller_enabled = (
                    not controller_enabled
                )

                if controller_enabled:

                    game_controller.enable()

                    print()
                    print("=" * 45)
                    print("CONTROLLER ENABLED")
                    print("Hand movements control the game.")
                    print("Fist activates hoverboard.")
                    print("=" * 45)

                else:

                    game_controller.disable()

                    motion_tracker.reset()

                    fist_detector.reset()

                    print()
                    print("=" * 45)
                    print("CONTROLLER DISABLED")
                    print("Keyboard control stopped.")
                    print("=" * 45)

            # ------------------------------------------------
            # Q = QUIT
            # ------------------------------------------------

            elif key == ord("q"):

                print()
                print("Q pressed. Exiting...")

                break

    except KeyboardInterrupt:

        print()
        print("Program interrupted.")

    finally:

        # ==================================================
        # CLEANUP
        # ==================================================

        print()
        print("Stopping controller...")

        game_controller.stop()

        detector.close()

        camera.release()

        cv2.destroyAllWindows()

        print("GestureSurfer AI stopped safely.")


if __name__ == "__main__":
    main()