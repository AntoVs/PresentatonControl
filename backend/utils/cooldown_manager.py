import time


class CooldownManager:

    def __init__(self, cooldown=1.5):

        self.cooldown = cooldown

        self.last_trigger = 0

    def ready(self):

        current_time = time.time()

        if current_time - self.last_trigger > self.cooldown:

            self.last_trigger = current_time

            return True

        return False
