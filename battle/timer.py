import time


class Timer:
    def __init__(self):
        # Record the start time when the timer is created
        self.start_time = time.time()

        # Accumulated paused duration
        self.paused_time = 0

        # Flag indicating whether the timer is currently paused
        self.is_paused = False

        # Timestamp when the current pause started
        self.pause_start = None

    def time(self):
        """
        Get the elapsed time since the timer started,
        excluding any time during which the timer was paused.
        """
        if self.is_paused:
            # If paused, return the elapsed time up to pause moment
            return self.paused_time
        # Otherwise, return current elapsed time minus paused duration
        return time.time() - self.start_time - self.paused_time

    def pause(self):
        """
        Pause the timer.
        Records the time at which pause starts and sets paused flag.
        """
        if not self.is_paused:
            self.pause_start = time.time()
            self.is_paused = True

    def resume(self):
        """
        Resume the timer from pause.
        Calculates and accumulates the duration paused.
        """
        if self.is_paused:
            self.paused_time += time.time() - self.pause_start
            self.is_paused = False