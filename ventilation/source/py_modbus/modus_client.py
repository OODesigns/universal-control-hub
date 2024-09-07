from dataclasses import field

from pymodbus.client import ModbusBaseClient
from modbus.modbus_builder import ModbusBuilder
from modbus.modbus_reader import ModbusBitReader, ModbusWordReader
from modbus.modbus import ModbusInterface, ModbusData
from py_modbus.modbus_connection_manager import ModbusConnectionManager
from py_modbus.modbus_result import (PyModbusCoilResult, PyModbusDiscreteInputResult,
                                     PyModbusInputRegisterResult, PyModbusHoldingRegisterResult)
from utils.operation_response import OperationResponse


class ModbusClient(ModbusInterface):
    """
   ModbusClient class that inherits from frozen ModbusInterface.
   Declares client-related fields to be supplied later, after initialization.
   """
    _client: ModbusBaseClient = field(init=False)
    _client_manager: ModbusConnectionManager = field(init=False)
    _coils_reader: ModbusBitReader = field(init=False)
    _discrete_inputs: ModbusBitReader = field(init=False)
    _input_registers: ModbusWordReader = field(init=False)
    _holding_registers: ModbusWordReader = field(init=False)

    def __init__(self, client: ModbusBaseClient, builder: ModbusBuilder):

        # Call the parent constructor to initialize immutable fields
        super().__init__(builder)

        # Initialize mutable fields that don't affect the parent frozen class
        object.__setattr__(self, '_client', client)
        object.__setattr__(self, '_client_manager', ModbusConnectionManager(self._client))

        # Setting readers as mutable fields
        object.__setattr__(self, '_coils_reader', ModbusBitReader(
            read_function=lambda address, count: PyModbusCoilResult.create(
                self._client, address, count)
        ))

        object.__setattr__(self, '_discrete_inputs', ModbusBitReader(
            read_function=lambda address, count: PyModbusDiscreteInputResult.create(
                self._client, address, count)
        ))

        object.__setattr__(self, '_input_registers', ModbusWordReader(
            read_function=lambda address, count: PyModbusInputRegisterResult.create(
                self._client, address, count)
        ))

        object.__setattr__(self, '_holding_registers', ModbusWordReader(
            read_function=lambda address, count: PyModbusHoldingRegisterResult.create(
                self._client, address, count)
        ))

    async def connect(self) -> OperationResponse:
        return await self._client_manager.connect()

    def disconnect(self) -> OperationResponse:
        return self._client_manager.disconnect()

    async def read(self) -> ModbusData:
        return ModbusData(
            coils=await self._coils_reader.read(0, self.coil_size.value),
            discrete_inputs=await self._discrete_inputs.read(0, self.discrete_input_size.value),
            input_register=await self._input_registers.read(0, self.input_register_size.value),
            holding_register=await self._holding_registers.read(0, self.holding_register_size.value)
        )
