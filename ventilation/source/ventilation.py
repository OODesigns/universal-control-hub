from enum import Enum
from temperature import Temperature
from temperature_sensor import AbstractTemperatureSensor


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

    def set_setpoint_temperature(self, temp: Temperature):
        pass
