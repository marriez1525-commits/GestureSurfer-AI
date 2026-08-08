"""
main.py

GestureSurfer AI

Combines:
    Webcam
    MediaPipe hand tracking
    Movement detection
    Gesture classification
    Keyboard controller
"""

import cv2

from camera.camera import Camera
from camera.fps import FPSCounter

from vision.hand_detector import HandDetector
from vision.landmark_tracker import LandmarkTracker
from vision.motion_tracker import MotionTracker
from vision.gesture_classifier import GestureClassifier

from controller.game_controller import GameController

from config import ACTION_NONE


def main():

    # ======================================================
    # INITIALIZE COMPONENTS
    # ======================================================

    camera = Camera()

    detector = HandDetector()

    landmark_tracker = LandmarkTracker()

    motion_tracker = MotionTracker()

    gesture_classifier = GestureClassifier()

    game_controller = GameController()

    fps_counter = FPSCounter()

    # ======================================================
    # START MESSAGE
    # ======================================================

    print("=" * 55)
    print("              GESTURESURFER AI")
    print("              FULL SYSTEM TEST")
    print("=" * 55)

    print()
    print("Hand controls:")
    print("    Move LEFT  -> Left Arrow")
    print("    Move RIGHT -> Right Arrow")
    print("    Move UP    -> Up Arrow")
    print("    Move DOWN  -> Down Arrow")
    print()
    print("Press Q to quit.")
    print("=" * 55)

    # ======================================================
    # MAIN LOOP
    # ======================================================

    try:

        while True:

            # ------------------------------------------------
            # Read camera
            # ------------------------------------------------

            frame = camera.read()

            if frame is None:

                print("Could not read camera frame.")

                break

            # ------------------------------------------------
            # Detect hand
            # ------------------------------------------------

            frame, landmarks = detector.process(frame)

            action = ACTION_NONE

            # ------------------------------------------------
            # Hand detected
            # ------------------------------------------------

            if landmarks is not None:

                # Give landmarks to tracker
                landmark_tracker.update(landmarks)

                # Get stable palm position
                palm_position = (
                    landmark_tracker.get_palm_center()
                )

                # Detect movement
                movement = motion_tracker.update(
                    palm_position
                )

                # Convert movement into action
                action = gesture_classifier.classify(
                    movement
                )

                # ------------------------------------------------
                # Send action to keyboard controller
                # ------------------------------------------------

                if action != ACTION_NONE:

                    game_controller.execute(action)

            else:

                # No hand detected
                gesture_classifier.reset()

            # ==================================================
            # DISPLAY INFORMATION
            # ==================================================

            fps = fps_counter.update()

            # FPS
            cv2.putText(
                frame,
                f"FPS: {fps:.1f}",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            # Hand status
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

            # Current action
            cv2.putText(
                frame,
                f"ACTION: {action}",
                (20, 115),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                3
            )

            # Controller status
            if game_controller.is_enabled():

                cv2.putText(
                    frame,
                    "CONTROLLER: ON",
                    (20, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

            else:

                cv2.putText(
                    frame,
                    "CONTROLLER: OFF",
                    (20, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2
                )

            # ------------------------------------------------
            # Show camera
            # ------------------------------------------------

            cv2.imshow(
                "GestureSurfer AI",
                frame
            )

            # ------------------------------------------------
            # Quit with Q
            # ------------------------------------------------

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):

                break

    except KeyboardInterrupt:

        print()
        print("Program stopped.")

    finally:

        # ==================================================
        # CLEANUP
        # ==================================================

        game_controller.stop()

        detector.close()

        camera.release()

        cv2.destroyAllWindows()

        print()
        print("GestureSurfer AI stopped safely.")


if __name__ == "__main__":
    main()