# 🏄‍♂️ GestureSurfer AI

GestureSurfer AI is an enterprise-grade computer vision and machine learning framework designed to transform a standard optical webcam into a high-precision, touchless motion-capture gaming controller. By tracking real-time spatial hand telemetry and modeling velocity dynamics, the application translates physical gestures into native hardware-level keyboard inputs, allowing users to control fast-paced endless runner games like *Subway Surfers* with zero physical contact.

---

## 🎯 Key Capabilities

* **21-Point Anatomical Tracking Matrix:** Leverages deep-learning pipeline architectures to map and track 21 distinct spatial landmarks across the hand framework (fingertips, knuckles, and wrist joints), maintaining tracking lock across variable lighting and high-contrast environments.
* **Concurrent Real-Time Execution:** Built on an optimized asynchronous processing pipeline that ingests video matrices, executes neural inference models, and injects OS-level keypresses with sub-millisecond latencies to minimize critical input lag.
* **Velocity Vectoring & Jitter Suppression:** Implements a localized calculus layer to measure rapid hand displacement and acceleration across a virtual Cartesian grid, filtering out micro-tremors, nervous shaking, or stray movements to validate deliberate execution intent.
* **Intelligent HUD & Coordinate Telemetry:** Renders a high-tech visual skeleton graph directly over the webcam stream overlay, supplying the developer or user with instant telemetry output strings (e.g., `[TRIGGER: JUMP]`) for accurate calibration.
* **Spatial Calibration & Distant Scaling:** Automatically handles horizontal frame mirroring for intuitive user navigation and scales spatial boundaries dynamically, allowing full tracking reliability whether the user is situated close to or far from the sensor.

---

## 🛠️ Technical Architecture & Ecosystem

The framework relies on a modular, decoupled Python system architecture engineered for optimized machine learning operations at the edge:

* **Perception Engine:** `MediaPipe Hands` (Deep learning inference pipeline) & `OpenCV` (Video capture, preprocessing, and matrix translation)
* **Mathematical Operations:** `NumPy` (High-speed vector calculations and geometric coordinate mapping)
* **OS Interfacing:** `PyAutoGUI` (Direct hardware-level keystroke emulation and system input mapping)

### Project Architecture
```text
GestureSurferAI/
│
├── main.py              # System entry point and orchestration loop
├── core/
│   ├── __init__.py
│   ├── tracking.py      # Telemetry extraction and anatomical landmark mapping
│   └── input_driver.py  # Emulation engine and native keyboard simulation
│
├── utils/
│   ├── __init__.py
│   └── filters.py       # Cartesian displacement metrics and jitter cancellation
│
└── requirements.txt     # System dependency manifest