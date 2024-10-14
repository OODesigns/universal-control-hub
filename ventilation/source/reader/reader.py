from abc import ABCMeta, abstractmethod


class Reader(metaclass=ABCMeta):
    @abstractmethod
    def read(self):
        """
        Perform a read operation on the device and return the result as an integer.
        :return:
        """
        pass