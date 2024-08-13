from abc import ABC, abstractmethod

from ventilation.source.temperature import Temperature


class AbstractTemperatureSensor(ABC):
    @abstractmethod
    def get_temperature(self) -> Temperature:
        """
        Gets the temperature. Must be overridden by child classes.

        :return: The temperature value.
        """
        pass
