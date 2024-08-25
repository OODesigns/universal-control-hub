from pymodbus import ModbusException
from pymodbus.client import AsyncModbusTcpClient
from devices.device_factory import DeviceFactory
from modbus.modbus import ModbusInterface


@DeviceFactory.register_dependency('modbus_tcp')
class ModbusTCP(ModbusInterface):
    def __init__(self, builder):
        from modbus.modbus_tcp_builder import ModbusTCPBuilder

        if not isinstance(builder, ModbusTCPBuilder):
            raise ValueError("builder must be an instance of ModbusTCPBuilder")

        super().__init__(builder)
        self._builder = builder
        self._client = None

    @property
    def client(self) -> AsyncModbusTcpClient:
        return self._client

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

    async def disconnect(self):
        self.client.close()


    async def read(self):
        try:
            data = await self.client.read_input_registers(0, self._builder.input_register_size.value-1)
            var = data.registers[1]

            data1 = await self.client.read_coils(0, self._builder.coil_size.value-1)
            var1 = data1.bits[1]

            data2 = await self.client.read_holding_registers(0, self._builder.holding_register_size.value-1)
            var2 = data2.bits[1]

            data3 = await self.client.read_discrete_inputs(0, self._builder.discrete_input_size.value-1)
            var3 = data3.bits[1]


        except ModbusException as e:
            # Handle the ModbusException here
            print(f"ModbusException occurred: {e}")
            return None  # or you can return an appropriate value or raise the exception


        # try:
        # # See all calls in client_calls.py
        # rr = await client.read_coils(1, 1, slave=1)
        #     except ModbusException as exc:
        #     print(f"Received ModbusException({exc}) from library")
        #     client.close()
        #     return
        # if rr.isError():
        #     print(f"Received Modbus library error({rr})")
        #     client.close()
        #     return
        # if isinstance(rr, ExceptionResponse):
        #     print(f"Received Modbus library exception ({rr})")
        #     # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        #     client.close()

