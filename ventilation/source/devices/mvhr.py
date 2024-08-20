from config.config_loader import ConfigLoader
from devices.device import Device
from devices.device_factory import DeviceFactory
from devices.modbus import ModbusInterface
from state.state_manager import StateManager
from utils.temperaturecelsius import TemperatureInterface, TemperatureCelsius


@DeviceFactory.register_device('mvhr')
class MVHR(Device):
    required_dependencies = ['modbus']  # This device requires a Modbus instance

    def __init__(self, config_loader: ConfigLoader, state_manager: StateManager, modus: ModbusInterface):
        super().__init__(config_loader, state_manager)
        self.modus = modus

    @property
    def temp_supply_in(self) -> TemperatureInterface:
        return TemperatureCelsius(0)

    @property
    def temp_supply_out(self) -> TemperatureInterface:
        return TemperatureCelsius(0)