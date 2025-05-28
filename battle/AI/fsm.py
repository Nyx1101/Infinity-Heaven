# ai/fsm.py

from typing import Callable, Dict

class FSM:
    def __init__(self):
        self.states: Dict[str, Callable[[], None]] = {}
        self.current: str = ""

    def add_state(self, name: str, fn: Callable[[], None]) -> None:
        self.states[name] = fn

    def set_state(self, name: str) -> None:
        if name in self.states:
            self.current = name

    def update(self) -> None:
        if self.current in self.states:
            self.states[self.current]()