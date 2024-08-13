from abc import ABC, abstractmethod


class AbstractValue(ABC):
    def __init__(self):
        self._value = None

    @property
    def value(self):
        return self._value

    def __eq__(self, other):
        if type(self) is type(other):
            return self.value == other.value
        return False
