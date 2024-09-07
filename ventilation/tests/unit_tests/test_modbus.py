import unittest
from typing import List
from unittest.mock import MagicMock
from modbus.modbus import ModbusInterface, ModbusData
from modbus.modbus_values import (CoilSize, DiscreteInputSize, InputRegisterSize, HoldingRegisterSize)
from utils.operation_response import OperationResponse
from utils.response import Response, ResponseStatus


# Creating a concrete subclass for testing purposes
class TestModbusInterfaceConcrete(ModbusInterface):
    async def connect(self) -> OperationResponse:
        return await super().connect()

    def disconnect(self) -> OperationResponse:
        return super().disconnect()

    async def read(self) -> ModbusData:
        return await super().read()


class TestModbusInterface(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Mocking the ModbusBuilder with specific attributes
        builder = MagicMock()
        builder.timeout = 1.0
        builder.retries = 3
        builder.reconnect_delay_max = 300.0
        builder.reconnect_delay = 0.1
        builder.coil_size = CoilSize(10)
        builder.discrete_input_size = DiscreteInputSize(20)
        builder.input_register_size = InputRegisterSize(30)
        builder.holding_register_size = HoldingRegisterSize(40)

        # Instantiating the concrete subclass for testing
        self.modbus_interface = TestModbusInterfaceConcrete(builder)

    async def test_coil_size(self):
        result = self.modbus_interface.coil_size
        self.assertEqual(result, CoilSize(10))

    async def test_discrete_input_size(self):
        result = self.modbus_interface.discrete_input_size
        self.assertEqual(result, DiscreteInputSize(20))

    async def test_input_register_size(self):
        result = self.modbus_interface.input_register_size
        self.assertEqual(result, InputRegisterSize(30))

    async def test_holding_register_size(self):
        result = self.modbus_interface.holding_register_size
        self.assertEqual(result, HoldingRegisterSize(40))


class TestModbusData(unittest.TestCase):

    def setUp(self):
        # Mock Response for different registers with ResponseStatus and explicit types
        self.valid_input_register = Response[List[int]](status=ResponseStatus.OK, details="", value=[100, 200, 300])
        self.valid_holding_register = Response[List[int]](status=ResponseStatus.OK, details="", value=[10, 20, 30])
        self.valid_discrete_inputs = Response[List[bool]](status=ResponseStatus.OK, details="", value=[True, False, True])
        self.valid_coils = Response[List[bool]](status=ResponseStatus.OK, details="", value=[False, True, False])

        # Initialize ModbusData with these responses
        self.modbus_data = ModbusData(
            input_register=self.valid_input_register,
            holding_register=self.valid_holding_register,
            discrete_inputs=self.valid_discrete_inputs,
            coils=self.valid_coils
        )

    def test_input_register(self):
        # Ensure the input_register property returns the correct list of integers and correct status
        result = self.modbus_data.input_register
        self.assertEqual(result.value, [100, 200, 300])
        self.assertEqual(result.status, ResponseStatus.OK)

    def test_holding_register(self):
        # Ensure the holding_register property returns the correct list of integers and correct status
        result = self.modbus_data.holding_register
        self.assertEqual(result.value, [10, 20, 30])
        self.assertEqual(result.status, ResponseStatus.OK)

    def test_discrete_inputs(self):
        # Ensure the discrete_inputs property returns the correct list of booleans and correct status
        result = self.modbus_data.discrete_inputs
        self.assertEqual(result.value, [True, False, True])
        self.assertEqual(result.status, ResponseStatus.OK)

    def test_coils(self):
        # Ensure the coils property returns the correct list of booleans and correct status
        result = self.modbus_data.coils
        self.assertEqual(result.value, [False, True, False])
        self.assertEqual(result.status, ResponseStatus.OK)

    def test_error_response(self):
        # Test a case where the response has an error status with the correct type
        error_response = Response[None](status=ResponseStatus.EXCEPTION, details="Error", value=None)
        # noinspection PyTypeChecker
        modbus_data = ModbusData(
            input_register=error_response,
            holding_register=error_response,
            discrete_inputs=error_response,
            coils=error_response
        )

        # Verify that all statuses are EXCEPTION
        self.assertEqual(modbus_data.input_register.status, ResponseStatus.EXCEPTION)
        self.assertEqual(modbus_data.holding_register.status, ResponseStatus.EXCEPTION)
        self.assertEqual(modbus_data.discrete_inputs.status, ResponseStatus.EXCEPTION)
        self.assertEqual(modbus_data.coils.status, ResponseStatus.EXCEPTION)


if __name__ == "__main__":
    unittest.main()
