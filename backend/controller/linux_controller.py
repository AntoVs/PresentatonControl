import os

from backend.controller.base_controller import \
    BaseController


class LinuxController(BaseController):

    def next_slide(self):

        os.system(
            "ydotool key 106:1 106:0"
        )

    def previous_slide(self):

        os.system(
            "ydotool key 105:1 105:0"
        )
