from abc import abstractmethod

from devices.device import Device
from utils.temperature import Temperature


class AbstractTemperatureSensor(Device):
    @abstractmethod
    def get_temperature(self) -> Temperature:
        """
        Gets the temperature. Must be overridden by child classes.

        :return: The temperature value.
        """
        pass
