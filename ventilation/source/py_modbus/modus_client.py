from pymodbus.client import ModbusBaseClient
from modbus.modbus_builder import ModbusBuilder
from modbus.modbus_reader import ModbusBitReader, ModbusWordReader
from modbus.modbus import ModbusInterface, ModbusData
from py_modbus.modbus_connection_manager import ModbusConnectionManager
from py_modbus.py_modbus_result import (PyModbusCoilResult, PyModbusDiscreteInputResult,
                                        PyModbusInputRegisterResult, PyModbusHoldingRegisterResult)
from utils.connection_reponse import ConnectionResponse


class ModbusClient(ModbusInterface):
    def __init__(self, client: ModbusBaseClient, builder: ModbusBuilder):
        super().__init__(builder)
        self._client = client
        self._client_manager = ModbusConnectionManager(self._client)

        self._coils_reader = ModbusBitReader(
            read_function=lambda address, count: PyModbusCoilResult.create(
                self._client, address, count)
        )
        self._discrete_inputs = ModbusBitReader(
            read_function=lambda address, count: PyModbusDiscreteInputResult.create(
                self._client, address, count)
        )
        self._input_registers = ModbusWordReader(
            read_function=lambda address, count: PyModbusInputRegisterResult.create(
                self._client, address, count)
        )
        self._holding_registers = ModbusWordReader(
            read_function=lambda address, count: PyModbusHoldingRegisterResult.create(
                self._client, address, count)
        )

    async def connect(self) -> ConnectionResponse:
        return await self._client_manager.connect()

    def disconnect(self) -> ConnectionResponse:
        return self._client_manager.disconnect()

    async def read(self) -> ModbusData:
        return ModbusData(
            _coils=await self._coils_reader.read(0, self.coil_size.value),
            _discrete_inputs=await self._discrete_inputs.read(0, self.discrete_input_size.value),
            _input_register=await self._input_registers.read(0, self.input_register_size.value),
            _holding_register=await self._holding_registers.read(0, self.holding_register_size.value)
        )
