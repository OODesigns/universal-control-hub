from enum import Enum

from ventilation.abstract_value import AbstractValue
from ventilation.temperature_sensor import AbstractTemperatureSensor


class Temperature(AbstractValue):
    def get_value(self):
        pass

    def __init__(self, value: int):
        super().__init__()
        if not (0 <= value <= 50):
            raise ValueError("Temperature must be between 0 and 50°C.")
        self.value = value

    def __int__(self):
        return self.value


class VentilationMode(Enum):
    EXCHANGE = 1
    COOLING = 2


class Ventilation:
    def __init__(self, outside_temp_sensor: AbstractTemperatureSensor):
        self.mode = None
        self.outside_temp_sensor = outside_temp_sensor

    def set_mode(self, mode: VentilationMode):
        self.mode = mode

    def get_mvhr_temp_before(self) -> Temperature:
        return Temperature(0)

    def get_mvhr_temp_after(self) -> Temperature:
        return Temperature(0)
