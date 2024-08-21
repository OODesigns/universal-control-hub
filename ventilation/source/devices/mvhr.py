import asyncio
from abc import abstractmethod

from config.config_loader import ConfigLoader
from devices.device import Device
from devices.modbus import ModbusFactory, ModbusInterface
from state.state_manager import StateManager
from utils.temperaturecelsius import TemperatureInterface, TemperatureCelsius

MAX_RETRIES_REACHED = 'Max retries reached'
MVHR_CONNECTION_FAILURE = 'mvhr_connection_failure'
MVHR_CONNECTED = 'mvhr_connected'
MVHR_TIMEOUT = 'mvhr-timeout'
MVHR_PORT = 'mvhr-port'
MVHR_IP_ADDRESS = 'mvhr-ip-address'

class MVHR(Device):
    def __init__(self, config_loader: ConfigLoader, state_manager: StateManager, modbus_factory: ModbusFactory):
        super().__init__(config_loader, state_manager)
        self._modbus_factory = modbus_factory

        # Retry configuration
        self.max_retries = 5
        self.base_delay = 1  # Start with a 1-second delay
        self.max_delay = 60  # Max delay between retries

    @property
    @abstractmethod
    def get_modbus(self)->ModbusInterface:
        pass

    @property
    def temp_supply_in(self) -> TemperatureInterface:
        return TemperatureCelsius(0)

    @property
    def temp_supply_out(self) -> TemperatureInterface:
        return TemperatureCelsius(0)

    async def start(self):
        """
        Start the MVHR device connection process, retrying if necessary.
        """
        success = self.connect_with_retries()
        if success:
            print("Successfully connected to the MVHR device.")
        else:
            print("Failed to connect to the MVHR device after multiple attempts.")

    async def connect_with_retries(self):
        retries = 0
        while retries < self.max_retries:
            try:
                # Attempt to connect
                self.get_modbus.connect()
                self._state_manager.update_state(
                    operational_states={MVHR_CONNECTED: True}
                )
                return True  # Connection successful
            except Exception as e:
                # Log failure in the state manager
                self._state_manager.update_state(
                    operational_states={MVHR_CONNECTED: False},
                    triggered_rules={MVHR_CONNECTION_FAILURE: str(e)}
                )

                retries += 1
                delay = min(self.base_delay * (2 ** (retries - 1)), self.max_delay)
                await asyncio.sleep(delay)  # Non-blocking delay

        # If we reach here, all retries failed
        self._state_manager.update_state(
            operational_states={MVHR_CONNECTED: False},
            triggered_rules={MVHR_CONNECTION_FAILURE: MAX_RETRIES_REACHED}
        )
        return False