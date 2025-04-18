from pymodbus.client.tcp import AsyncModbusTcpClient

from py_modbus.modus_py_client import ModbusPYClient


class ModbusTCPClient(ModbusPYClient):
    def __init__(self, builder):
        # Lazy import to avoid circular dependency
        from modbus.modbus_tcp_client_builder import ModbusTCPClientBuilder

        assert isinstance(builder, ModbusTCPClientBuilder), "builder must be an instance of ModbusTCPBuilder"

        client = AsyncModbusTcpClient(
            host=builder.ip_address.value,
            port=builder.port.value,
            timeout=builder.timeout.value,
            reconnect_delay=builder.reconnect_delay.value,
            reconnect_delay_max=builder.reconnect_delay_max.value,
            retries=builder.retries.value
        )
        super().__init__(client, builder)
