from modbus.modbus_builder import ModbusBuilder
from modbus.modbus_tcp import ModbusTCP
from utils.tcp_values import IPAddress, Port

class ModbusTCPBuilder(ModbusBuilder):
    def __init__(self, builder: ModbusBuilder = None):
        super().__init__(builder)
        self._ip_address = None
        self._port = None

    @property
    def ip_address(self) -> IPAddress:
        return self._ip_address

    @property
    def port(self) -> Port:
        return self._port

    def set_ip_address(self, ip_address: IPAddress):
        if not isinstance(ip_address, IPAddress):
            raise ValueError("Invalid IP address")
        self._ip_address = ip_address
        return self

    def set_port(self, port: Port):
        if not isinstance(port, Port):
            raise ValueError("Invalid port")
        self._port = port
        return self

    def build(self):
        if not self._ip_address:
            raise ValueError("IP address must be set for ModbusTCP")
        if not self._port:
            raise ValueError("Port must be set for ModbusTCP")
        return ModbusTCP(self)
