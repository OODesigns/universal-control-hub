from modbus.modbus_tcp_client_builder import ModbusTCPClientBuilder
from modbus.modus_rtu_client_builder import ModbusRTUClientBuilder
from py_modbus.modbus_rtu_client import ModbusRTUClient
from py_modbus.modbus_tcp_client import ModbusTCPClient

ModbusTCPClientBuilder.register_client(client_class= ModbusTCPClient)
ModbusRTUClientBuilder.register_client(client_class= ModbusRTUClient)
