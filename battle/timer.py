import time


class Timer:
    def __init__(self):
        self.start_time = time.time()
        self.paused_time = 0
        self.is_paused = False
        self.pause_start = None

    def time(self):
        if self.is_paused:
            return self.paused_time
        return time.time() - self.start_time - self.paused_time

    def pause(self):
        if not self.is_paused:
            self.pause_start = time.time()
            self.is_paused = True

    def resume(self):
        if self.is_paused:
            self.paused_time += time.time() - self.pause_start
            self.is_paused = False
