from abc import ABC, abstractmethod


class AbstractValue(ABC):
    def __init__(self):
        self.value = None

    @abstractmethod
    def get_value(self):
        return self.value
