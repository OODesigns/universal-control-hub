from pymodbus.client import AsyncModbusSerialClient
from devices.device_factory import DeviceFactory
from modbus.pymodbus.modus_base import ModbusBase

@DeviceFactory.register_dependency('modbus_rtu')
class ModbusRTU(ModbusBase):
    def __init__(self, builder):
        # Lazy import to avoid circular dependency
        from modbus.modus_rtu_builder import ModbusRTUBuilder

        if not isinstance(builder, ModbusRTUBuilder):
            raise ValueError("builder must be an instance of ModbusRTUBuilder")

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
