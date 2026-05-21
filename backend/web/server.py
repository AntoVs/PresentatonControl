from flask import Flask
from flask import render_template

from flask_socketio import \
    SocketIO

import cv2
import base64


class GestureSlideServer:

    def __init__(self, gesture_app):

        self.gesture_app = gesture_app

        self.app = Flask(
            __name__,
            template_folder="../../frontend/templates",
            static_folder="../../frontend/static"
        )

        self.socketio = SocketIO(
            self.app,
            cors_allowed_origins="*"
        )

        self.setup_routes()


    def setup_routes(self):

        @self.app.route("/")
        def index():

            return render_template(
                "index.html"
            )


    def stream_frame(self):

        frame = \
            self.gesture_app.current_frame

        if frame is None:
            return

        _, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        frame_base64 = \
            base64.b64encode(
                buffer
            ).decode("utf-8")

        state = self.gesture_app.state

        self.socketio.emit(
            "video_frame",
            {

                "frame":
                    frame_base64,

                "gesture":
                    state.current_gesture,

                "action":
                    state.current_action,

                "locked":
                    state.system_locked
            }
        )


    def run(self):

        print(
            "[SERVER] Flask Started"
        )

        self.socketio.run(
            self.app,
            host="0.0.0.0",
            port=5000,
            debug=False,
            use_reloader=False
        )
