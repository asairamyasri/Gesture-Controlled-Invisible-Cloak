# Gesture-Controlled Invisible Cloak using OpenCV

This project implements a **real-time gesture-controlled invisible cloak effect** using **Python and OpenCV**.  
Hand gestures detected through a webcam are used to control different system states, enabling an interactive invisibility effect.

---

## Features
- Real-time **hand gesture detection**
- Gesture-based mode switching:
  - **2 fingers** → Activate cloak mode (invisibility)
  - **Automatic timeout** → Return to normal mode
  - **5 fingers** → Forced exit / override
- Smooth transition between normal and cloak modes

---

## Technologies Used
- Python
- OpenCV
- MediaPipe (for hand landmark detection)

---

## How It Works
1. The background is captured initially. (Run the "images.py" file to save your background first)
2. Hand gestures are detected in real time using hand landmarks. 
3. Specific gestures trigger state changes:
   - Cloak mode activation
   - Automatic timeout
   - Manual forced exit
4. The cloak effect replaces the detected cloak region with the stored background.

---
