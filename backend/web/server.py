from flask import Flask
from flask import render_template
from flask import Response
from flask import jsonify

import cv2
import time

class GestureSlideServer:

    def __init__(self, gesture_app):

        self.gesture_app = gesture_app

        self.app = Flask(
            __name__,
            template_folder="../../frontend/templates",
            static_folder="../../frontend/static"
        )

        self.setup_routes()

    # ===================================
    # ROUTES
    # ===================================

    def setup_routes(self):

        @self.app.route("/")
        def index():

            return render_template(
                "index.html"
            )

        @self.app.route("/video_feed")
        def video_feed():

            return Response(
                self.generate_frames(),
                mimetype=(
                    "multipart/x-mixed-replace;"
                    " boundary=frame"
                )
            )

        @self.app.route("/status")
        def status():

            state = self.gesture_app.state

            return jsonify({

                "gesture":
                    state.current_gesture,

                "action":
                    state.current_action,

                "locked":
                    state.system_locked
            })

    # ===================================
    # FRAME STREAM
    # ===================================

    def generate_frames(self):

        while True:

            frame = \
                self.gesture_app.current_frame

            if frame is None:
                time.sleep(0.01)
                continue

            _, buffer = cv2.imencode(
                ".jpg",
                frame
            )

            frame_bytes = buffer.tobytes()

            yield (

                b"--frame\r\n"

                b"Content-Type: image/jpeg\r\n\r\n"

                + frame_bytes +

                b"\r\n"
            )

    # ===================================
    # RUN SERVER
    # ===================================

    def run(self):

        self.app.run(
            host="0.0.0.0",
            port=5000,
            debug=False,
            use_reloader=False
        )
