# ai/blackboard.py

class Blackboard:
    def __init__(self):
        self.data: dict[str, any] = {}

    def set(self, key: str, value: any) -> None:
        self.data[key] = value

    def get(self, key: str) -> any:
        return self.data.get(key)

    def has(self, key: str) -> bool:
        return key in self.data