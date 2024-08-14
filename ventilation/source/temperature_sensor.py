from abc import ABC, abstractmethod

from device import Device
from ventilation.source.temperature import Temperature


class AbstractTemperatureSensor(Device):
    @abstractmethod
    def get_temperature(self) -> Temperature:
        """
        Gets the temperature. Must be overridden by child classes.

        :return: The temperature value.
        """
        pass
