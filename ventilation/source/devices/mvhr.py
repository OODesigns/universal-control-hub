from config.config_loader import ConfigLoader
from devices.device import Device
from devices.modbus import ModbusFactory
from state.state_manager import StateManager
from utils.temperaturecelsius import TemperatureInterface, TemperatureCelsius


class MVHR(Device):
    def __init__(self, config_loader: ConfigLoader, state_manager: StateManager, modbus: ModbusFactory):
        super().__init__(config_loader, state_manager)
        self._modbus = modbus

    @property
    def temp_supply_in(self) -> TemperatureInterface:
        return TemperatureCelsius(0)

    @property
    def temp_supply_out(self) -> TemperatureInterface:
        return TemperatureCelsius(0)