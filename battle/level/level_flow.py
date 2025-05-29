from collections import deque


class LevelFlow:
    def __init__(self, spawn_schedule):
        self.flow = deque(sorted(spawn_schedule, key=lambda x: x["time"]))

    def pop_next_if_due(self, current_time):
        if self.flow and self.flow[0]["time"] <= current_time:
            return self.flow.popleft()
        return None

    def has_remaining(self):
        return bool(self.flow)
