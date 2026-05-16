class GestureClassifier:

    def __init__(self):

        self.tip_ids = [4, 8, 12, 16, 20]

    def get_finger_states(self, landmarks):

        fingers = []

        if len(landmarks) == 0:
            return fingers

        # -----------------------------
        # Thumb
        # -----------------------------
        # Compare thumb tip and joint x position
        # Works for mirrored webcam feed

        if landmarks[4][1] < landmarks[3][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # -----------------------------
        # Other 4 Fingers
        # -----------------------------

        for tip_id in [8, 12, 16, 20]:

            tip_y = landmarks[tip_id][2]
            pip_y = landmarks[tip_id - 2][2]

            if tip_y < pip_y:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def classify_gesture(self, fingers):

        if len(fingers) != 5:
            return "Unknown"

        # Open Palm
        if fingers == [1, 1, 1, 1, 1]:
            return "Open Palm"

        # Fist
        elif fingers == [0, 0, 0, 0, 0]:
            return "Fist"

        # Index Finger
        elif fingers == [0, 1, 0, 0, 0]:
            return "Index Finger"

        # Peace
        elif fingers == [0, 1, 1, 0, 0]:
            return "Peace"

        return "Unknown"
