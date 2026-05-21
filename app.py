import os
import time
import threading

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["GLOG_minloglevel"] = "3"

import cv2

from backend.state.system_state import SystemState
from backend.gestures.hand_tracker import HandTracker
from backend.gestures.gesture_classifier import GestureClassifier
from backend.controller.slide_controller import get_controller
from backend.controller.pointer_controller import PointerController
from backend.utils.cooldown_manager import CooldownManager
from backend.web.server import \
    GestureSlideServer


class GestureSlideApp:
    def __init__(self):

        self.cap = cv2.VideoCapture(0)
        self.tracker = HandTracker()
        self.classifier = GestureClassifier()
        self.slide_controller = get_controller()
        self.pointer_controller = PointerController()
        self.cooldown = CooldownManager(1.5)
        self.state = SystemState()
        self.current_frame = None

        # WEB SERVER
        self.server = GestureSlideServer(
            self
        )

        # POINTER SETTINGS
        self.prev_hand_x = 0
        self.prev_hand_y = 0
        self.pointer_speed = 2.5
        self.movement_threshold = 8
        self.prev_time = 0

    # MAIN LOOP
    def run(self):

        # START WEB SERVER
        def start_server():

            try:

                self.server.run()

            except Exception as e:

                print(
                    "[SERVER ERROR]"
                )

                print(e)

        server_thread = threading.Thread(
            target=start_server
        )

        server_thread.daemon = True

        server_thread.start()

        try:

            while True:

                success, frame = \
                    self.cap.read()

                if not success:
                    break

                # MIRROR WEBCAM

                frame = cv2.flip(
                    frame,
                    1
                )

                # ===================================
                # HAND TRACKING
                # ===================================

                frame, landmarks = \
                    self.tracker.process_frame(
                        frame
                    )

                # ===================================
                # GESTURE DETECTION
                # ===================================

                self.detect_gesture(
                    landmarks
                )

                # ===================================
                # ACTION PROCESSING
                # ===================================

                self.process_actions(
                    landmarks
                )

                fps = self.calculate_fps()

                self.render_ui(
                    frame,
                    fps
                )


                self.current_frame = \
                    frame.copy()

                self.server.stream_frame()

        except KeyboardInterrupt:

            print(
                "Exiting GestureSlide..."
            )

        finally:

            self.cleanup()

    # ===================================
    # GESTURE DETECTION
    # ===================================

    def detect_gesture(self, landmarks):

        self.state.current_gesture = \
            "NONE"

        if landmarks:

            fingers = \
                self.classifier.get_finger_states(
                    landmarks
                )

            self.state.current_gesture = \
                self.classifier.classify_gesture(
                    fingers
                )

    # ===================================
    # ACTION PROCESSING
    # ===================================

    def process_actions(self, landmarks):

        gesture = \
            self.state.current_gesture

        # ===================================
        # LOCK SYSTEM
        # ===================================

        if gesture == "LOCK":

            self.toggle_lock()

            return

        # ===================================
        # STOP IF LOCKED
        # ===================================

        if self.state.system_locked:
            return

        # ===================================
        # POINTER MODE
        # ===================================

        if gesture == "POINTER" and landmarks:

            self.handle_pointer(
                landmarks
            )

            return

        # ===================================
        # SLIDE CONTROLS
        # ===================================

        if self.cooldown.ready():

            if gesture == "NEXT":

                self.next_slide()

            elif gesture == "BACK":

                self.previous_slide()

    # ===================================
    # LOCK SYSTEM
    # ===================================

    def toggle_lock(self):

        if self.cooldown.ready():

            self.state.system_locked = \
                not self.state.system_locked

            if self.state.system_locked:

                self.state.current_action = \
                    "SYSTEM LOCKED"

            else:

                self.state.current_action = \
                    "SYSTEM ACTIVE"

            print(
                f"[SYSTEM] "
                f"{self.state.current_action}"
            )

    # ===================================
    # POINTER HANDLING
    # ===================================

    def handle_pointer(self, landmarks):

        self.state.current_action = \
            "POINTER MODE"

        x = landmarks[8][1]
        y = landmarks[8][2]

        movement_x = \
            x - self.prev_hand_x

        movement_y = \
            y - self.prev_hand_y

        self.prev_hand_x = x
        self.prev_hand_y = y

        if abs(movement_x) > \
           self.movement_threshold or \
           abs(movement_y) > \
           self.movement_threshold:

            dx = int(
                movement_x *
                self.pointer_speed
            )

            dy = int(
                movement_y *
                self.pointer_speed
            )

            self.pointer_controller.move(
                dx,
                dy
            )

    # NEXT SLIDE

    def next_slide(self):

        self.state.current_action = \
            "NEXT SLIDE"

        print(
            "[ACTION] NEXT SLIDE"
        )

        self.slide_controller.next_slide()

    # PREVIOUS SLIDE

    def previous_slide(self):

        self.state.current_action = \
            "PREVIOUS SLIDE"

        print(
            "[ACTION] PREVIOUS SLIDE"
        )

        self.slide_controller.previous_slide()

    def calculate_fps(self):

        current_time = time.time()

        time_diff = \
            current_time - self.prev_time

        fps = int(
            1 / time_diff
        ) if time_diff > 0 else 0

        self.prev_time = current_time

        return fps

    def get_ui_color(self):

        action = \
            self.state.current_action

        if "NEXT" in action:

            return (0, 255, 255)

        elif "PREVIOUS" in action:

            return (255, 0, 255)

        elif "POINTER" in action:

            return (0, 255, 0)

        elif "LOCKED" in action:

            return (0, 0, 255)

        return (255, 255, 255)

    def render_ui(
        self,
        frame,
        fps
    ):

        color = self.get_ui_color()

        cv2.rectangle(
            frame,
            (20, 20),
            (760, 190),
            color,
            2
        )

        self.draw_text(
            frame,
            "GestureSlide",
            (260, 40),
            (0, 255, 255),
            0.9
        )

        self.draw_text(
            frame,
            f"GESTURE : "
            f"{self.state.current_gesture}",
            (40, 80),
            color,
            0.9
        )

        self.draw_text(
            frame,
            f"ACTION  : "
            f"{self.state.current_action}",
            (40, 125),
            color,
            0.9
        )

        status = \
            "LOCKED" \
            if self.state.system_locked \
            else "ACTIVE"

        self.draw_text(
            frame,
            f"STATUS : {status}",
            (40, 170),
            (255, 255, 255),
            0.8
        )

        self.draw_text(
            frame,
            f"FPS : {fps}",
            (frame.shape[1] - 170, 40),
            (0, 255, 0),
            0.8
        )

    def draw_text(
        self,
        frame,
        text,
        position,
        color,
        scale
    ):

        cv2.putText(
            frame,
            text,
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            scale,
            color,
            2
        )


    def cleanup(self):

        self.cap.release()

        cv2.destroyAllWindows()

if __name__ == "__main__":

    app = GestureSlideApp()

    app.run()
