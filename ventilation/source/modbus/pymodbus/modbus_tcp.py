from pymodbus.client import AsyncModbusTcpClient
from devices.device_factory import DeviceFactory
from modbus.pymodbus.modus_base import ModbusBase

@DeviceFactory.register_dependency('modbus_tcp')
class ModbusTCP(ModbusBase):
    def __init__(self, builder):
        # Lazy import to avoid circular dependency
        from modbus.modbus_tcp_builder import ModbusTCPBuilder

        if not isinstance(builder, ModbusTCPBuilder):
            raise ValueError("builder must be an instance of ModbusTCPBuilder")

        client = AsyncModbusTcpClient(
            host=builder.ip_address.value,
            port=builder.port.value,
            timeout=builder.timeout.value,
            reconnect_delay=builder.reconnect_delay.value,
            reconnect_delay_max=builder.reconnect_delay_max.value,
            retries=builder.retries.value
        )
        super().__init__(client, builder)
