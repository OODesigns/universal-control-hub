from config.config_store import ConfigStore
from utils.temperaturecelsius import TemperatureInterface
from ventilation_mode import VentilationMode


class VentilationConfiguration:
    def __init__(self, store: ConfigStore):
        self._store = store

    @property
    def ventilation_mode(self) -> VentilationMode:
        return self._store.get_value("ventilation_mode")

    @ventilation_mode.setter
    def ventilation_mode(self, value: VentilationMode ):
        self._store.set_value("ventilation_mode", value)

    @property
    def setpoint_temperature(self) ->TemperatureInterface:
        return self._store.get_value('setpoint_temperature')

    @setpoint_temperature.setter
    def setpoint_temperature(self, value: TemperatureInterface):
        self._store.set_value('setpoint_temperature' , value)

