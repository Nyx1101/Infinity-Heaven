from abc import ABC, abstractmethod
from entities.entity import Entity


class IAI(ABC):
    def __init__(self):
        self.entity = Entity

    @abstractmethod
    def update(self):
        pass
