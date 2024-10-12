from abc import ABC, abstractmethod

class DeviceReader(ABC):
    """
    Abstract interface to represent a device reader .
    """
    @abstractmethod
    def read(self) -> int:
        """
        Perform a read operation on the device and return the result as an integer.
        :return:
        """
        pass
