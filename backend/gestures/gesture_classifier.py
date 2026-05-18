class GestureClassifier:

    def get_finger_states(self, landmarks):

        fingers = []

        tip_ids = [4, 8, 12, 16, 20]

        # Thumb

        if landmarks[tip_ids[0]][1] < \
           landmarks[tip_ids[0] - 1][1]:

            fingers.append(1)

        else:

            fingers.append(0)

        # Other fingers

        for i in range(1, 5):

            if landmarks[tip_ids[i]][2] < \
               landmarks[tip_ids[i] - 2][2]:

                fingers.append(1)

            else:

                fingers.append(0)

        return fingers

    def classify_gesture(self, fingers):

        # Open Palm

        if fingers == [1, 1, 1, 1, 1]:
            return "NEXT"

        # Index Finger

        elif fingers == [0, 1, 0, 0, 0]:
            return "POINTER"

        # Pinky Finger

        elif fingers == [0, 0, 0, 0, 1]:
            return "BACK"

        # Fist

        elif fingers == [0, 0, 0, 0, 0]:
            return "LOCK"

        return "NONE"
