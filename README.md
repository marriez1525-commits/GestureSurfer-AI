# 🏄‍♂️ GestureSurfer AI

## 📝 Project Introduction
**GestureSurfer AI** is an innovative, high-performance computer vision application engineered to bridge the gap between physical human movement and digital gaming environments. By transforming a standard computer webcam into an intelligent input device, this project enables users to control the popular, fast-paced endless runner game *Subway Surfers* entirely through real-time hand gestures. 

Traditional gaming relies heavily on physical keyboards, mice, or controllers. **GestureSurfer AI** replaces these hardware dependencies by deploying a highly optimized artificial intelligence pipeline that tracks hand movements and translates them into instantaneous system-level keyboard events. The core framework is built entirely in Python, utilizing advanced machine learning models to capture spatial data frames, analyze anatomical landmarks, and calculate directional velocity. Whether running on a web-browser version of the game or a desktop emulator, the application delivers an immersive, hands-free, and incredibly responsive gaming experience without requiring any modifications to the game itself.

---

## ✨ Advanced Features

### 🚀 High-Fidelity 21-Point Hand Tracking
The backbone of the system relies on deep-learning-based perception pipelines that detect and trace a complex structure of 21 distinct structural landmarks across the human hand. This allows the application to maintain rock-solid tracking accuracy even under varying ambient lighting conditions, busy backgrounds, or minor camera angles.

### ⚡ Sub-Millisecond Gesture Telemetry
To succeed in a high-speed game like *Subway Surfers*, timing is everything. The application features a lightweight processing pipeline that minimizes frame-analysis latency. Optical data is ingested, processed, and mapped to hardware-level keystrokes within milliseconds, ensuring that your jumps, ducks, and lane switches happen exactly when you intend them to.

### 🧠 Intelligent Vector-Based Gesture Logic
Instead of relying on rigid, static hand poses, the system utilizes dynamic vector tracking. By measuring the rapid displacement and directional velocity of the hand's center point along the Cartesian coordinate plane, it can precisely distinguish an intentional game-play swipe from ordinary, passive hand movements or natural camera jitter.

### 🖥️ Real-Time Head-Up Display (HUD)
The application opens a sleek, integrated feedback window overlaying the live webcam feed. This HUD renders real-time visual tracking data, drawing a digital skeleton over the user's hand and displaying active bounding boxes. A status indicator text immediately updates to show which gesture is being triggered, serving as a valuable tool for user calibration and debugging.

### 🔄 Automatic Mirror Correction & Scaling
Webcam feeds are naturally inverted, which can make physical movement counter-intuitive. The preprocessing script automatically flips the incoming image matrices horizontally, ensuring that moving your physical hand to the left translates to a leftward lane change on the screen. Additionally, the tracking thresholds scale dynamically based on your hand's distance from the camera lens to prevent accidental triggers.