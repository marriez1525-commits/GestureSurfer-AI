import cv2

from camera.camera import Camera
from camera.fps import FPSCounter

from vision.hand_detector import HandDetector
from vision.landmark_tracker import LandmarkTracker
from vision.motion_tracker import MotionTracker
from vision.gesture_classifier import GestureClassifier


def main():

    # --------------------------------------------------------
    # Initialize components
    # --------------------------------------------------------

    camera = Camera()

    detector = HandDetector()

    landmark_tracker = LandmarkTracker()

    motion_tracker = MotionTracker()

    gesture_classifier = GestureClassifier()

    fps_counter = FPSCounter()

    print("======================================")
    print("       GestureSurfer AI")
    print("       Gesture Test Mode")
    print("======================================")
    print()
    print("Move your hand:")
    print("LEFT  -> Move hand left")
    print("RIGHT -> Move hand right")
    print("UP    -> Move hand up")
    print("DOWN  -> Move hand down")
    print()
    print("Press Q to quit.")
    print()

    # --------------------------------------------------------
    # Main loop
    # --------------------------------------------------------

    while True:

        frame = camera.read()

        if frame is None:
            print("Could not read camera frame.")
            break

        # ----------------------------------------------------
        # Detect hand
        # ----------------------------------------------------

        frame, landmarks = detector.process(frame)

        action = "NONE"

        # ----------------------------------------------------
        # If hand detected
        # ----------------------------------------------------

        if landmarks is not None:

            # Give landmarks to tracker
            landmark_tracker.update(landmarks)

            # Get palm center
            palm_position = landmark_tracker.get_palm_center()

            # Detect movement
            movement = motion_tracker.update(palm_position)

            # Convert movement to game action
            action = gesture_classifier.classify(movement)

        else:

            # No hand
         gesture_classifier.reset()
            

        # ----------------------------------------------------
        # FPS
        # ----------------------------------------------------

        fps = fps_counter.update()

        # ----------------------------------------------------
        # Display information
        # ----------------------------------------------------

        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # Hand status
        if detector.is_hand_detected():

            cv2.putText(
                frame,
                "HAND DETECTED",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

        else:

            cv2.putText(
                frame,
                "NO HAND",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        # ----------------------------------------------------
        # Display current action
        # ----------------------------------------------------

        cv2.putText(
            frame,
            f"ACTION: {action}",
            (20, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 0),
            3
        )

        # ----------------------------------------------------
        # Show window
        # ----------------------------------------------------

        cv2.imshow(
            "GestureSurfer AI - Gesture Test",
            frame
        )

        # Q = quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # --------------------------------------------------------
    # Cleanup
    # --------------------------------------------------------

    detector.close()
    camera.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()