import cv2
import mediapipe as mp


class HandTracker:
    def __init__(self,
                 mode=False,
                 max_hands=1,
                 detection_confidence=0.7,
                 tracking_confidence=0.7):

        self.mode = mode
        self.max_hands = max_hands

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

        self.mp_draw = mp.solutions.drawing_utils

    def process_frame(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb)

        landmarks = []

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

                for idx, lm in enumerate(hand_landmarks.landmark):

                    h, w, _ = frame.shape

                    cx = int(lm.x * w)
                    cy = int(lm.y * h)

                    landmarks.append((idx, cx, cy))

        return frame, landmarks
