from abc import ABC, abstractmethod

class IAI(ABC):
    @abstractmethod
    def update(self) -> None:
        pass