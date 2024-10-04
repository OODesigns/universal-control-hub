from abc import ABC, abstractmethod

from spi.spi import SPIInterface

class SPIClient(SPIInterface, ABC):

    @abstractmethod
    def __init__(self, builder):
        pass
