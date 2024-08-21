from config.config_loader import ConfigLoader
from devices.device_factory import DeviceFactory
from devices.modbus import ModbusFactory, ModbusMode, ModbusInterface
from devices.mvhr import MVHR, MVHR_IP_ADDRESS, MVHR_PORT, MVHR_TIMEOUT
from devices.blauberg_registers import CoilRegister, DiscreteInputs, InputRegisters, HoldingRegister
from state.state_manager import StateManager
from utils.tcp_values import IPAddress, Port, Timeout


@DeviceFactory.register_device('blauberg_mvhr')
class BlaubergMVHR(MVHR):
    required_dependencies = ['modbus']

    def __init__(self, config_loader: ConfigLoader, state_manager: StateManager, modbus_factory: ModbusFactory):
        super().__init__(config_loader, state_manager, modbus_factory)

        self._modbus = self._modbus_factory.create_modbus(mode=ModbusMode.TCP,
                                   coil_size=CoilRegister.CL_SIZE.value,
                                   discrete_input_size=DiscreteInputs.DI_SIZE.value,
                                   input_register_size=InputRegisters.IR_SIZE.value,
                                   holding_register_size=HoldingRegister.HR_SIZE.value,
                                   ip_address=IPAddress(config_loader.get_value(MVHR_IP_ADDRESS)),
                                   port=Port(config_loader.get_value(MVHR_PORT)),
                                   timeout=Timeout(config_loader.get_value(MVHR_TIMEOUT)))

    @property
    def get_modbus(self) -> ModbusInterface:
        return self._modbus




