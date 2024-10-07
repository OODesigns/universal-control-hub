from abc import ABC, abstractmethod

from config.config_loader import ConfigLoader


class DeviceReader(ABC):
    """
    Abstract interface to represent a device reader .
    """

    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader

    @abstractmethod
    def read(self) -> int:
        """
        Perform a read operation on the device and return the result as an integer.
        :return:
        """
        pass
