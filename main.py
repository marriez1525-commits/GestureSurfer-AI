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
    SPACE = Controller ON/OFF
    Q     = Quit

Hand gestures:
    Swipe LEFT  = Left Arrow
    Swipe RIGHT = Right Arrow
    Swipe UP    = Jump
    Swipe DOWN  = Roll
    Fist        = Hoverboard
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
    # CONTROLLER STARTS OFF
    # ======================================================

    controller_enabled = False

    game_controller.disable()

    # ======================================================
    # STARTUP MESSAGE
    # ======================================================

    print("=" * 55)
    print("              GESTURESURFER AI")
    print("=" * 55)

    print()

    print("Hand Controls:")
    print("    Move LEFT  -> Left Arrow")
    print("    Move RIGHT -> Right Arrow")
    print("    Move UP    -> Up Arrow")
    print("    Move DOWN  -> Down Arrow")
    print("    FIST       -> Hoverboard")

    print()

    print("Keyboard Controls:")
    print("    SPACE -> Controller ON/OFF")
    print("    Q     -> Quit")

    print()

    print("The controller is currently OFF.")

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
                # Get palm center
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
                # Convert movement to action
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
                # Send keyboard action
                # --------------------------------------------

                if (
                    controller_enabled
                    and action != ACTION_NONE
                ):

                    game_controller.execute(
                        action
                    )

            # ------------------------------------------------
            # HAND NOT FOUND
            # ------------------------------------------------

            else:

                gesture_classifier.reset()

                fist_detector.reset()

            # ==================================================
            # GET FPS
            # ==================================================

            fps = fps_counter.update()

            # ==================================================
            # GET MOVEMENT DEBUG VALUES
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
            # DISPLAY HAND STATUS
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
            # DISPLAY MOVEMENT VALUES
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
            # DISPLAY ACTION
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
            # DISPLAY CONTROLLER STATUS
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
            # DISPLAY INSTRUCTIONS
            # ==================================================

            cv2.putText(
                frame,
                "SPACE = ON/OFF",
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
            # SPACE = TOGGLE CONTROLLER
            # ------------------------------------------------

            if key == ord(" "):

                controller_enabled = (
                    not controller_enabled
                )

                if controller_enabled:

                    game_controller.enable()

                    print()
                    print("=" * 40)
                    print("CONTROLLER ENABLED")
                    print("Hand movements control the keyboard.")
                    print("FIST activates the hoverboard.")
                    print("=" * 40)

                else:

                    game_controller.disable()

                    motion_tracker.reset()

                    fist_detector.reset()

                    print()
                    print("=" * 40)
                    print("CONTROLLER DISABLED")
                    print("Hand movements do not control keyboard.")
                    print("=" * 40)

            # ------------------------------------------------
            # Q = QUIT
            # ------------------------------------------------

            elif key == ord("q"):

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