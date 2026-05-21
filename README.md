# Presentation Control

Real-time presentation control system built using MediaPipe, OpenCV, Flask, and WebSockets.
Control presentation slides and pointer movement using hand gestures.

---

## Features

- Real-time hand tracking
- Gesture-based slide navigation
- Pointer control (Relative)
- Lock / unlock system
- FPS monitoring
  
---

# Gestures

| Gesture | Action |
|---|---|
| Open Palm | Next Slide |
| Pinky Finger | Previous Slide |
| Index Finger | Pointer Mode |
| Fist | Lock / Unlock System |

---

## Backend

- Python
- OpenCV
- MediaPipe
- Flask
- Flask-SocketIO

## Frontend

- HTML
- CSS
- JavaScript

---

# File Structure

```bash

├── app.py
├── backend
│   ├── controller
│   │   ├── base_controller.py
│   │   ├── linux_controller.py
│   │   ├── pointer_controller.py
│   │   └── slide_controller.py
│   ├── gestures
│   │   ├── gesture_classifier.py
│   │   └── hand_tracker.py
│   ├── state
│   │   └── system_state.py
│   ├── utils
│   │   └── cooldown_manager.py
│   └── web
│       └── server.py
├── frontend
│   └── templates
│       └── index.html
├── README.md
├── requirements.txt
└── run.sh
```
---

# Dependencies

```bash

python 3.11
ydotools [current implimentation for linux System]

```
## Installation

```bash

git clone --depth 1 https://github.com/AntoVs/PresentatonControl.git
cd PresentatonControl
pip install -r requirements.txt

sudo pacman -S ydotool v4l-utils  #Arch
sudo apt install ydotool          #Debian Based Systems

chmod +x run.sh
./run.sh
#run the server

```

---

# ScreenShots
<img width="1920" height="1200" alt="image" src="https://github.com/user-attachments/assets/6f0a9112-07e2-466b-897e-cc23fb84db47" />
