from pymodbus.client import AsyncModbusSerialClient
from modbus.pymodbus.modus_client import ModbusClient

class ModbusRTU(ModbusClient):
    def __init__(self, builder):
        # Lazy import to avoid circular dependency
        from modbus.modus_rtu_builder import ModbusRTUBuilder

        assert isinstance(builder, ModbusRTUBuilder), "builder must be an instance of ModbusRTUBuilder"

        client = AsyncModbusSerialClient(
            port=builder.serial_port.value,
            baudrate=builder.baud_rate.value,
            parity=builder.parity.value,
            stopbits=builder.stop_bits.value,
            timeout=builder.timeout.value,
            reconnect_delay=builder.reconnect_delay.value,
            reconnect_delay_max=builder.reconnect_delay_max.value,
            retries=builder.retries.value
        )
        super().__init__(client, builder)
