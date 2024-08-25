from config.config_loader import ConfigLoader
from devices.device_factory import DeviceFactory
from devices.blauberg_registers import CoilRegister, DiscreteInputs, InputRegisters, HoldingRegister
from devices.mvhr import MVHR
from modbus.modbus import MODBUS, ModbusInterface, ModbusMode
from modbus.modbus_builder import ModbusBuilder
from modbus.modbus_factory import ModbusFactory
from state.state_manager import StateManager
from utils.tcp_values import IPAddress, Port
from utils.modbus_values import Timeout, Retries, ReconnectDelay, ReconnectDelayMax, CoilSize, DiscreteInputSize, InputRegisterSize, HoldingRegisterSize

MVHR_PORT = 'mvhr-port'
MVHR_IP_ADDRESS = 'mvhr-ip-address'
MVHR_TIMEOUT = 'mvhr-timeout'
MVHR_RETRIES = 'mvhr-retries'
MVHR_RECONNECT_DELAY = 'mvhr-reconnect-delay'
MVHR_RECONNECT_DELAY_MAX = 'mvhr-reconnect-delay-max'

@DeviceFactory.register_device('blauberg_mvhr')
class BlaubergMVHR(MVHR):
    async def read_data(self):
        pass

    required_dependencies = [MODBUS]

    def __init__(self, config_loader: ConfigLoader, state_manager: StateManager, modbus_factory: ModbusFactory):
        super().__init__(config_loader, state_manager, modbus_factory)

        # Create a ModbusBuilder with common settings using specific size objects
        modbus_builder = ModbusBuilder()
        modbus_builder.set_coil_size(CoilSize(CoilRegister.CL_SIZE.value))
        modbus_builder.set_discrete_input_size(DiscreteInputSize(DiscreteInputs.DI_SIZE.value))
        modbus_builder.set_input_register_size(InputRegisterSize(InputRegisters.IR_SIZE.value))
        modbus_builder.set_holding_register_size(HoldingRegisterSize(HoldingRegister.HR_SIZE.value))

        # Set modbus settings from the configuration loader
        modbus_builder.set_timeout(Timeout(config_loader.get_value(MVHR_TIMEOUT)))
        modbus_builder.set_retries(Retries(config_loader.get_value(MVHR_RETRIES)))
        modbus_builder.set_reconnect_delay(ReconnectDelay(config_loader.get_value(MVHR_RECONNECT_DELAY)))
        modbus_builder.set_reconnect_delay_max(ReconnectDelayMax(config_loader.get_value(MVHR_RECONNECT_DELAY_MAX)))

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
