import unittest
from unittest.mock import MagicMock

from modbus.modbus import ModbusInterface, ModbusData
from modbus.modbus_values import (CoilSize, DiscreteInputSize,
                                  InputRegisterSize, HoldingRegisterSize)
from utils.operation_response import OperationResponse
from utils.value import ValidatedResponse, ValueStatus


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
        # Test coil_size property
        result = self.modbus_interface.coil_size
        self.assertEqual(result, CoilSize(10))

    async def test_discrete_input_size(self):
        # Test discrete_input_size property
        result = self.modbus_interface.discrete_input_size
        self.assertEqual(result, DiscreteInputSize(20))

    async def test_input_register_size(self):
        # Test input_register_size property
        result = self.modbus_interface.input_register_size
        self.assertEqual(result, InputRegisterSize(30))

    async def test_holding_register_size(self):
        # Test holding_register_size property
        result = self.modbus_interface.holding_register_size
        self.assertEqual(result, HoldingRegisterSize(40))

class TestModbusData(unittest.TestCase):

    def setUp(self):
        # Mock ValidatedResponse for different registers
        self.valid_input_register = ValidatedResponse(status=ValueStatus.OK, details="", value=[100, 200, 300])
        self.valid_holding_register = ValidatedResponse(status=ValueStatus.OK, details="", value=[10, 20, 30])
        self.valid_discrete_inputs = ValidatedResponse(status=ValueStatus.OK, details="", value=[True, False, True])
        self.valid_coils = ValidatedResponse(status=ValueStatus.OK, details="", value=[False, True, False])

        # Initialize ModbusData with these validated responses
        self.modbus_data = ModbusData(
            _input_register=self.valid_input_register,
            _holding_register=self.valid_holding_register,
            _discrete_inputs=self.valid_discrete_inputs,
            _coils=self.valid_coils
        )

    def test_input_register(self):
        # Ensure the input_register property returns the correct list of integers
        result = self.modbus_data.input_register
        self.assertEqual(result, [100, 200, 300])

    def test_holding_register(self):
        # Ensure the holding_register property returns the correct list of integers
        result = self.modbus_data.holding_register
        self.assertEqual(result, [10, 20, 30])

    def test_discrete_inputs(self):
        # Ensure the discrete_inputs property returns the correct list of booleans
        result = self.modbus_data.discrete_inputs
        self.assertEqual(result, [True, False, True])

    def test_coils(self):
        # Ensure the coils property returns the correct list of booleans
        result = self.modbus_data.coils
        self.assertEqual(result, [False, True, False])
