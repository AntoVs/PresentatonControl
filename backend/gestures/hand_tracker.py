import cv2
import mediapipe as mp


class HandTracker:

    def __init__(self):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )

        self.mp_draw = mp.solutions.drawing_utils

    def process_frame(self, frame):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = self.hands.process(rgb_frame)

        landmarks = []

        if results.multi_hand_landmarks:

            for hand_landmarks in \
                    results.multi_hand_landmarks:

                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

                for id, landmark in \
                        enumerate(hand_landmarks.landmark):

                    h, w, c = frame.shape

                    cx = int(landmark.x * w)
                    cy = int(landmark.y * h)

                    landmarks.append([id, cx, cy])

        return frame, landmarks
