from abc import ABC, abstractmethod
from utils.temperaturecelsius import TemperatureInterface

class MVHRRepositoryInterface(ABC):
    @property
    @abstractmethod
    def temp_supply_in(self) -> TemperatureInterface:
        """
        This property should return the temperature interface object representing
        the supply air temperature coming into the MVHR system.
        """
        pass

    @property
    @abstractmethod
    def temp_supply_out(self) -> TemperatureInterface:
        """
        This property should return the temperature interface object representing
        the supply air temperature going out of the MVHR system.
        """
        pass

