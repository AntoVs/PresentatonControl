import cv2
import time

from backend.gestures.hand_tracker import HandTracker
from backend.gestures.gesture_classifier import GestureClassifier
from backend.gestures.swipe_detector import SwipeDetector

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

tracker = HandTracker()
classifier = GestureClassifier()
swipe_detector = SwipeDetector()

prev_time = 0

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame, landmarks = tracker.process_frame(frame)

    gesture = "No Hand"

    if landmarks:

        fingers = classifier.get_finger_states(landmarks)
        gesture = classifier.classify_gesture(fingers)
        swipe = swipe_detector.detect_swipe(landmarks)
        if swipe:
            gesture = swipe

    # FPS Calculation
    current_time = time.time()
    fps = 1 / (current_time - prev_time) if prev_time != 0 else 0
    prev_time = current_time

    # Gesture Text
    symbol = ""

    if gesture == "Swipe Right":
        symbol = "->"

    elif gesture == "Swipe Left":
        symbol = "<-"
    elif gesture == "Open Palm":
        symbol = "PALM"
    elif gesture == "Fist":
        symbol = "LOCK"
    elif gesture == "Index Finger":
        symbol = "DRAW"

    cv2.putText(
        frame,
        symbol,
        (250, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        2,
        (0, 255, 255),
        4
    )

    # FPS Text
    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    cv2.imshow("GestureSlide", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
