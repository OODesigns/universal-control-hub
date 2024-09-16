from modbus.modbus_tcp_builder import ModbusTCPBuilder
from modbus.modus_rtu_builder import ModbusRTUBuilder
from py_modbus.modbus_rtu import ModbusRTU
from py_modbus.modbus_tcp import ModbusTCP

ModbusTCPBuilder.register_modbus(client_class= ModbusTCP)
ModbusRTUBuilder.register_modbus(client_class= ModbusRTU)
