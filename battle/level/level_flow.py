from collections import deque


class LevelFlow:
    def __init__(self, schedule):
        """
        Initialize LevelFlow with a schedule of enemy spawn events.
        """
        self.flow = self._preprocess_schedule(schedule)

    def _preprocess_schedule(self, schedule):
        """
        Flatten and sort the schedule entries by time, expanding any entries with multiple times.
        """
        expanded = []
        for entry in schedule:
            times = entry["time"]
            if not isinstance(times, list):
                times = [times]  # Normalize to list
            for t in times:
                expanded.append({
                    "id": entry["id"],
                    "time": t,
                    "path": entry["path"]
                })
        # Sort by spawn time ascending
        expanded.sort(key=lambda x: x["time"])
        return deque(expanded)

    def pop_next_if_due(self, current_time):
        """
        Pop and return the next scheduled event if its time is due.
        """
        if self.flow and self.flow[0]["time"] <= current_time:
            return self.flow.popleft()
        return None

    def has_remaining(self):
        """
        Check if there are remaining scheduled events.
        """
        return bool(self.flow)
