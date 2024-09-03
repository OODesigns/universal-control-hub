from blauberg.blauberg_mvhr_state import BlaubergMVHRState
from blauberg.blauberg_registers import CoilRegister, DiscreteInputs, InputRegisters, HoldingRegister
from config.config_loader import ConfigLoader
from devices.mvhr import MVHR
from modbus.modbus import MODBUS, ModbusInterface, ModbusMode
from modbus.modbus_builder import ModbusBuilder
from modbus.modbus_factory import ModbusFactory
from mvhr_state import MVHRStateInterface
from utils.connection_reponse import ConnectionResponse
from modbus.tcp_values import IPAddress, Port
import modbus.modbus_values

MVHR_PORT = 'mvhr-port'
MVHR_IP_ADDRESS = 'mvhr-ip-address'
MVHR_TIMEOUT = 'mvhr-timeout'
MVHR_RETRIES = 'mvhr-retries'
MVHR_RECONNECT_DELAY = 'mvhr-reconnect-delay'
MVHR_RECONNECT_DELAY_MAX = 'mvhr-reconnect-delay-max'

class BlaubergMVHR(MVHR):
    required_dependencies = [MODBUS]

    def __init__(self, config_loader: ConfigLoader, modbus_factory: ModbusFactory):
        super().__init__(config_loader)
        self._modbus_factory = modbus_factory

        # Create a ModbusBuilder with common settings using specific size objects
        modbus_builder = ModbusBuilder()
        modbus_builder.set_coil_size(modbus.modbus_values.CoilSize(CoilRegister.CL_SIZE.value))
        modbus_builder.set_discrete_input_size(modbus.modbus_values.DiscreteInputSize(DiscreteInputs.DI_SIZE.value))
        modbus_builder.set_input_register_size(modbus.modbus_values.InputRegisterSize(InputRegisters.IR_SIZE.value))
        modbus_builder.set_holding_register_size(
            modbus.modbus_values.HoldingRegisterSize(HoldingRegister.HR_SIZE.value))

        # Set modbus settings from the configuration loader
        modbus_builder.set_timeout(modbus.modbus_values.Timeout(config_loader.get_value(MVHR_TIMEOUT)))
        modbus_builder.set_retries(modbus.modbus_values.Retries(config_loader.get_value(MVHR_RETRIES)))
        modbus_builder.set_reconnect_delay(
            modbus.modbus_values.ReconnectDelay(config_loader.get_value(MVHR_RECONNECT_DELAY)))
        modbus_builder.set_reconnect_delay_max(
            modbus.modbus_values.ReconnectDelayMax(config_loader.get_value(MVHR_RECONNECT_DELAY_MAX)))

        # Use the factory to create the Modbus interface
        self._modbus = self._modbus_factory.create_modbus(
            mode=ModbusMode.TCP,
            builder=modbus_builder,
            ip_address=IPAddress(config_loader.get_value(MVHR_IP_ADDRESS)),
            port=Port(config_loader.get_value(MVHR_PORT))
        )

    @property
    def modbus(self) -> ModbusInterface:
        return self._modbus

    async def read_data(self) -> MVHRStateInterface:
        return BlaubergMVHRState(await self._modbus.read())

    def stop(self) -> ConnectionResponse:
        return self.modbus.disconnect()

    async def start(self) -> ConnectionResponse:
        return await self.modbus.connect()
