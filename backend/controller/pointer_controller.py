import os


class PointerController:

    def move(self, dx, dy):

        command = \
            f"ydotool mousemove -- {dx} {dy}"

        os.system(command)
