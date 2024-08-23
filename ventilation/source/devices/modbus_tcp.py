from pymodbus.client import AsyncModbusTcpClient
from devices.device_factory import DeviceFactory
from devices.modbus import ModbusInterface


@DeviceFactory.register_dependency('modbus_tcp')
class ModbusTCP(ModbusInterface):
    def __init__(self, builder):
        from devices.modbus_tcp_builder import ModbusTCPBuilder

        if not isinstance(builder, ModbusTCPBuilder):
            raise ValueError("builder must be an instance of ModbusTCPBuilder")

        super().__init__(builder)
        self._builder = builder
        self._client = None

    async def connect(self):
        self._client = AsyncModbusTcpClient(
            host=self._builder.ip_address.value,
            port=self._builder.port.value,
            timeout=self._builder.timeout.value,
            reconnect_delay=self._builder.reconnect_delay.value,
            reconnect_delay_max=self._builder.reconnect_delay_max.value,
            retries=self._builder.retries.value
        )
        await self._client.connect()
