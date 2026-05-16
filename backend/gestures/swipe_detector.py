import time

class SwipeDetector:
    def __init__(self, threshold=120, cooldown=1):
        self.threshold = threshold
        self.cooldown = cooldown

        self.start_x = None
        self.last_swipe_time = 0

    def detect_swipe(self, landmarks):

        if len(landmarks) == 0:
            return None

        wrist_x = landmarks[0][1]

        current_time = time.time()

        # Initialize
        if self.start_x is None:
            self.start_x = wrist_x
            return None

        delta_x = wrist_x - self.start_x

        # Cooldown
        if current_time - self.last_swipe_time < self.cooldown:
            return None

        # Swipe Right
        if delta_x > self.threshold:

            self.last_swipe_time = current_time
            self.start_x = wrist_x

            return "Swipe Right"

        # Swipe Left
        elif delta_x < -self.threshold:

            self.last_swipe_time = current_time
            self.start_x = wrist_x

            return "Swipe Left"

        return None
