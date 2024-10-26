from abc import ABC, abstractmethod

from reader.reader import Reader, T
from utils.response import Response
from utils.standard_name import StandardName

class DeviceReader(Reader[T], ABC):
    """
    Abstract interface to represent a device reader.
    """
    def __init__(self, device_to_read: [StandardName]):
        # Device name will be set by the child class
        self.config_name: StandardName = StandardName(f"{self.get_device_name()}_{device_to_read.value}")

    @abstractmethod
    def get_device_name(self) -> str:
        """
        Abstract method for getting the device name. This will be implemented by child classes.
        :return:
        """

    def get_config_name(self) -> StandardName:
        return self.config_name

    @abstractmethod
    def read(self) -> Response[T]:
        """
        Abstract method for reading device. This will be implemented by child classes.
        :return:
        """

