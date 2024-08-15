from config.config_loader import ConfigLoader
from devices.device import Device
from devices.device_factory import DeviceFactory
from devices.modbus import ModbusInterface


@DeviceFactory.register_device('mvhr')
class MVHR(Device):
    required_dependencies = ['modbus']  # This device requires a Modbus instance

    def __init__(self, config_loader: ConfigLoader, modus: ModbusInterface):
        super().__init__(config_loader)
        self.modus = modus
