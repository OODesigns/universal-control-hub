from abc import ABC, abstractmethod


class AbstractTemperatureSensor(ABC):
    @abstractmethod
    def get_temperature(self) -> int:
        """
        Gets the temperature. Must be overridden by child classes.

        :return: The temperature value.
        """
        pass
