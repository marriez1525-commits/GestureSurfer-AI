🏃‍♂️ Subway Surfers: Hand Gesture Controller
An interactive computer vision project that allows users to play the popular game Subway Surfers using real-time hand gestures. By leveraging a standard webcam and AI-powered hand tracking, this application translates physical hand movements into keyboard inputs (Left, Right, Up, Down) to control the character seamlessly.

✨ Features
Real-time Hand Tracking: Uses high-fidelity landmarks to detect hand movements instantly.

Intuitive Gesture Controls: Mimics natural gameplay swiping:

☝️ Jump: Move your hand rapidly upward.

👇 Duck / Roll: Move your hand rapidly downward.

👈 Move Left: Swipe your hand to the left.

👉 Move Right: Swipe your hand to the right.

Virtual Key Mapping: Translates visual data into direct game inputs without modifying the game itself.

On-Screen Feedback: Visual indicators on the webcam feed show detected gestures and system status.

🛠️ Tech Stack & Dependencies
Language: Python

Computer Vision: OpenCV (for video capturing and image processing)

AI/ML Framework: MediaPipe (for robust 21-point hand landmark detection)

Keyboard Automation: PyAutoGUI / pynput (for triggering game controls)