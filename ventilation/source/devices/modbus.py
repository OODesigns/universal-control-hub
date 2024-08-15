from abc import ABC

from devices.device_factory import DeviceFactory


class ModbusInterface(ABC):
    pass

@DeviceFactory.register_dependency('modbus')
class Modbus(ModbusInterface):
    pass
