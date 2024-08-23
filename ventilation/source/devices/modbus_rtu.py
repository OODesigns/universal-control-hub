from enum import Enum
from pymodbus.client import AsyncModbusSerialClient
from devices.modbus import ModbusInterface
from devices.device_factory import DeviceFactory

class ParityType(Enum):
    NONE = 'N'
    EVEN = 'E'
    ODD = 'O'

@DeviceFactory.register_dependency('modbus_rtu')
class ModbusRTU(ModbusInterface):
    def __init__(self, builder):
        # Delay the import here to avoid circular import at module level
        from devices.modus_rtu_builder import ModbusRTUBuilder

        if not isinstance(builder, ModbusRTUBuilder):
            raise ValueError("builder must be an instance of ModbusRTUBuilder")

        super().__init__(builder)
        self._builder = builder
        self._client = None

    async def connect(self):
        self._client = AsyncModbusSerialClient(
            port=self._builder.serial_port.value,
            baudrate=self._builder.baud_rate.value,
            parity=self._builder.parity.value,
            stopbits=self._builder.stop_bits.value,
            timeout=self._builder.timeout.value,
            reconnect_delay=self._builder.reconnect_delay.value,
            reconnect_delay_max=self._builder.reconnect_delay_max.value,
            retries=self._builder.retries.value
        )
        await self._client.connect()

