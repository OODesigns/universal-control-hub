from abc import abstractmethod

from config.config_loader import ConfigLoader
from devices.device import Device
from devices.modbus import ModbusInterface
from devices.modbus_factory import ModbusFactory
from state.state_manager import StateManager
from utils.temperaturecelsius import TemperatureInterface, TemperatureCelsius

MVHR_CONNECTION_FAILURE = 'mvhr_connection_failure'
MVHR_CONNECTED = 'mvhr_connected'


class MVHR(Device):
    def __init__(self, config_loader: ConfigLoader, state_manager: StateManager, modbus_factory: ModbusFactory):
        super().__init__(config_loader, state_manager)
        self._modbus_factory = modbus_factory

    @property
    @abstractmethod
    def modbus(self) -> ModbusInterface:
        pass

    @property
    def temp_supply_in(self) -> TemperatureInterface:
        return TemperatureCelsius(0)

    @property
    def temp_supply_out(self) -> TemperatureInterface:
        return TemperatureCelsius(0)

    async def start(self):
        """
        Start the MVHR device connection process.
        """
        try:
            await self.modbus.connect()
            self._state_manager.update_state(operational_states={MVHR_CONNECTED: True})

        except Exception as e:
            self._state_manager.update_state(
                operational_states={MVHR_CONNECTED: False},
                triggered_rules={MVHR_CONNECTION_FAILURE: str(e)}
            )
