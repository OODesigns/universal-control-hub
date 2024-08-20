from config.config_loader import ConfigLoader
from devices.device_factory import DeviceFactory
from devices.modbus import ModbusFactory
from devices.mvhr import MVHR
from state.state_manager import StateManager

@DeviceFactory.register_device('blauberg-mvhr')
class BlaubergMVHR(MVHR):
    required_dependencies = ['modbus']

    def __init__(self, config_loader: ConfigLoader, state_manager: StateManager, modbus: ModbusFactory):
        super().__init__(config_loader, state_manager, modbus)

