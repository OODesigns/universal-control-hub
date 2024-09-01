from pymodbus.client import AsyncModbusTcpClient
from modbus.pymodbus.modus_client import ModbusClient

class ModbusTCP(ModbusClient):
    def __init__(self, builder):
        # Lazy import to avoid circular dependency
        from modbus.modbus_tcp_builder import ModbusTCPBuilder

        assert isinstance(builder, ModbusTCPBuilder), "builder must be an instance of ModbusTCPBuilder"

        client = AsyncModbusTcpClient(
            host=builder.ip_address.value,
            port=builder.port.value,
            timeout=builder.timeout.value,
            reconnect_delay=builder.reconnect_delay.value,
            reconnect_delay_max=builder.reconnect_delay_max.value,
            retries=builder.retries.value
        )
        super().__init__(client, builder)
