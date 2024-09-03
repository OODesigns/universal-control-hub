from devices.device_factory import DeviceFactory
from modbus.modbus import ModbusMode
from modbus.modbus_factory import ModbusFactory
from py_modbus.modbus_rtu import ModbusRTU
from py_modbus.modbus_tcp import ModbusTCP

ModbusFactory.register_modbus(mode=ModbusMode.TCP,client_class= ModbusTCP)
ModbusFactory.register_modbus(mode=ModbusMode.RTU,client_class= ModbusRTU)
DeviceFactory.register_dependency("modbus", ModbusFactory)