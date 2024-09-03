from typing import Type
from modbus.modbus_builder import ModbusBuilder
from modbus.tcp_values import IPAddress, Port
from modbus.modbus import ModbusInterface

class ModbusTCPBuilder(ModbusBuilder):
    def __init__(self, builder: ModbusBuilder = None, client_class: Type[ModbusInterface] = None):
        super().__init__(builder)
        self._ip_address = None
        self._port = None
        self._client_class = client_class  # Store the client class to instantiate later

    @property
    def ip_address(self) -> IPAddress:
        return self._ip_address

    @property
    def port(self) -> Port:
        return self._port

    def set_ip_address(self, ip_address: IPAddress):
        assert isinstance(ip_address, IPAddress), "Invalid IP address"
        self._ip_address = ip_address
        return self

    def set_port(self, port: Port):
        assert isinstance(port, Port), "Invalid port"
        self._port = port
        return self

    def build(self) -> ModbusInterface:
        assert self._ip_address, "IP address must be set for ModbusTCP"
        assert self._port, "Port must be set for ModbusTCP"
        return self._client_class(self)
