# GestureSurfer AI

**GestureSurfer AI** is an ultra-low-latency computer vision interface designed to translate real-world physical hand dynamics into hardware-level keyboard events. Engineered specifically for fast-paced endless runner titles like *Subway Surfers*, it utilizes deep learning perception pipelines to track hand spatial kinetics via a standard webcam—delivering zero-hardware-dependency spatial control.

---

## 🔑 Key Engineering Highlights

* **High-Fidelity Spatial Tracking:** Deploys deep neural networks to extract and track 21 key anatomical landmarks per hand at high frame rates, maintaining accuracy across dynamic ambient illumination and complex background noise.
* **Vector-Driven Motion Classification:** Replaces rigid static pose matching with a dynamic vector motion engine that evaluates temporal velocity ($\Delta x / \Delta t$, $\Delta y / \Delta t$) and Cartesian displacement to differentiate deliberate action swipes from ambient motion and sensor noise.
* **Near-Zero Latency Pipeline:** Features a stream-optimized frame ingestion, preprocessing, and spatial analytics loop designed to minimize processing overhead and ensure instantaneous OS-level input injection.
* **Real-Time Instrumentation HUD:** Visualizes optical feedback, topological skeletal wireframes, active motion vectors, and frame latency metrics via a transparent telemetry overlay.
* **Dynamic Coordinate Normalization:** Automatically applies horizontal matrix flipping for intuitive mirror mapping and dynamically scales gesture velocity thresholds based on optical depth (Z-distance).

---

## 🏗️ System Architecture

```text
  ┌─────────────────┐      ┌─────────────────────┐      ┌──────────────────────────┐
  │  Camera Frame   │ ───► │ Matrix Preprocess   │ ───► │ MediaPipe Landmark Engine│
  │   Ingestion     │      │ (Flip & Color Space)│      │  (21-Point 3D Vectors)   │
  └─────────────────┘      └─────────────────────┘      └────────────┬─────────────┘
                                                                     │
  ┌─────────────────┐      ┌─────────────────────┐                   │
  │ OS Key Event    │ ◄─── │ Event Dispatcher &  │ ◄─────────────────┘
  │ (PyAutoGUI/Win) │      │ Cooldown Queue      │ (Temporal Velocity Engine)
  └─────────────────┘      └─────────────────────┘