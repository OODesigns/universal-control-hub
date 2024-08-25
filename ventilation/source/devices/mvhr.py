import asyncio
from abc import abstractmethod
from config.config_loader import ConfigLoader
from devices.device import Device
from modbus.modbus import ModbusInterface
from modbus.modbus_factory import ModbusFactory
from state.state_manager import StateManager
from utils.temperaturecelsius import TemperatureInterface, TemperatureCelsius

MVHR_START_FAILURE = 'mvhr_start_failure'
MVHR_RUNNING = 'mvhr_running'

class MVHR(Device):
    def __init__(self, config_loader: ConfigLoader, state_manager: StateManager, modbus_factory: ModbusFactory):
        super().__init__(config_loader, state_manager)
        self._modbus_factory = modbus_factory
        self._stop_event = asyncio.Event()

    @property
    @abstractmethod
    def modbus(self) -> ModbusInterface:
        pass

    @abstractmethod
    async def read_data(self):
        pass

    async def poll_data(self, interval=1.0):
        while not self._stop_event.is_set():
            await self.read_data()
            await asyncio.sleep(interval)

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
            self._state_manager.update_state(operational_states={MVHR_RUNNING: True})
            #TODO move polling to ventilation class
            await self.poll_data()


        except Exception as e:
            self._state_manager.update_state(
                operational_states={MVHR_RUNNING: False},
                triggered_rules={MVHR_START_FAILURE: str(e)}
            )

    async def stop(self):
        self._stop_event.set()
        await self.modbus.disconnect()  # Assuming there is a disconnect method
        self._state_manager.update_state(operational_states={MVHR_RUNNING: False})
