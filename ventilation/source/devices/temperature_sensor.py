from abc import abstractmethod

from devices.device import Device
from utils.temperaturecelsius import TemperatureInterface


class TemperatureSensorInterface(Device):
    @abstractmethod
    def get_temperature(self) -> TemperatureInterface:
        """
        Gets the temperature. Must be overridden by child classes.

        :return: The temperature value.
        """
        pass
