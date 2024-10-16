from abc import abstractmethod, ABC
from typing import TypeVar, Generic

from utils.response import Response

T = TypeVar('T')

class Reader(Generic[T], ABC):
    @abstractmethod
    def read(self) ->Response[T] :
        """
        Perform a read operation on the device and return the result as an integer.
        :return:
        """
        pass