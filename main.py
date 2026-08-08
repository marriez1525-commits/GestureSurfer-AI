import cv2

from camera.camera import Camera
from camera.fps import FPSCounter
from vision.hand_detector import HandDetector


def main():

    camera = Camera()
    detector = HandDetector()
    fps_counter = FPSCounter()

    print("GestureSurfer AI started.")
    print("Show your hand to the camera.")
    print("Press Q to quit.")

    while True:

        frame = camera.read()

        if frame is None:
            print("Could not read camera frame.")
            break

        # Detect hand
        frame, landmarks = detector.process(frame)

        # FPS
        fps = fps_counter.update()

        # Display FPS
        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        # Display hand status
        if detector.is_hand_detected():

            cv2.putText(
                frame,
                "HAND DETECTED",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        else:

            cv2.putText(
                frame,
                "NO HAND",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2
            )

        # Show camera
        cv2.imshow("GestureSurfer AI - Test", frame)

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    detector.close()
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()