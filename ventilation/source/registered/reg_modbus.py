from devices.device_factory import DeviceFactory
from modbus.modbus_factory import ModbusFactory

DeviceFactory.register_dependency("modbus", ModbusFactory)