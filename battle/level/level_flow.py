from collections import deque


class LevelFlow:
    def __init__(self, schedule):
        self.flow = self._preprocess_schedule(schedule)

    def _preprocess_schedule(self, schedule):
        expanded = []
        for entry in schedule:
            times = entry["time"]
            if not isinstance(times, list):
                times = [times]
            for t in times:
                expanded.append({
                    "id": entry["id"],
                    "time": t,
                    "path": entry["path"]
                })
        expanded.sort(key=lambda x: x["time"])
        return deque(expanded)

    def pop_next_if_due(self, current_time):
        if self.flow and self.flow[0]["time"] <= current_time:
            return self.flow.popleft()
        return None

    def has_remaining(self):
        return bool(self.flow)
