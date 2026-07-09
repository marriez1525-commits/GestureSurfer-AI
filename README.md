# 🏄‍♂️ GestureSurfer AI

GestureSurfer AI is an advanced computer vision and machine learning framework designed to transform a standard webcam into a touchless, motion-capture gaming controller. By tracking real-time spatial hand telemetry, the application translates physical hand gestures into hardware-level keyboard inputs, allowing users to control fast-paced endless runner games like *Subway Surfers* entirely hands-free.

---

## 🚀 Key Features

* **21-Point Hand Telemetry Matrix:** Utilizes an advanced deep-learning perception model to track 21 distinct anatomical landmarks across the hand (fingertips, knuckles, and wrist joints), ensuring stable tracking under diverse environmental lighting conditions.
* **Ultra-Low Latency Inference:** Built on a concurrent data-processing loop that ingests frames, runs neural inference, and injects OS-level keypresses with sub-millisecond execution times to eliminate input lag.
* **Intelligent Anti-Jitter Filtering:** Measures acceleration and spatial displacement across a virtual Cartesian grid, filtering out micro-tremors or accidental movements to trigger inputs *only* on deliberate swipes.
* **Interactive HUD Overlay:** Features a live Head-Up Display (HUD) mapped onto the video capture window, rendering a real-time digital skeleton over the user's hand alongside active action cues (e.g., `[TRIGGER: JUMP]`).
* **Adaptive Mirroring & Distance Scaling:** Automatically mirrors the video feed for intuitive directional mapping and dynamically adjusts tracking thresholds based on the user's distance from the camera.

---

## 🛠️ System Architecture & Tech Stack

The application relies on a modular Python pipeline optimized for real-time edge processing:

* **Computer Vision & Tracking:** `OpenCV` (Video ingestion and image preprocessing) and `MediaPipe` (Hand landmark inference)
* **Input Injection:** `PyAutoGUI` / Native OS integration for direct, hardware-level keystroke emulation
* **Mathematical Optimization:** `NumPy` for high-speed spatial coordinate and velocity vector calculations

### Project Structure
```text
GestureSurferAI/
│
├── main.py              # Application entry point and main execution loop
├── core/
│   ├── __init__.py
│   ├── tracking.py      # MediaPipe hand tracking and landmark extraction
│   └── input_driver.py  # PyAutoGUI keyboard simulation logic
│
├── utils/
│   ├── __init__.py
│   └── filters.py       # Velocity vector calculations and jitter reduction
│
└── requirements.txt     # Project dependencies