import unittest
from abc import ABC

from modbus.modbus_builder import ModbusBuilder
from modbus.modbus_builder_client import ModbusBuilderClient
from modbus.modbus_values import CoilSize, DiscreteInputSize, InputRegisterSize, HoldingRegisterSize, Timeout, Retries, ReconnectDelay, ReconnectDelayMax
from utils.status import Status

# Mock Modbus client class for testing
class MockModbusClient(ModbusBuilderClient, ABC):
    def __init__(self, builder):
        pass

class TestModbusBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Register the mock Modbus client
        ModbusBuilder.register_modbus(MockModbusClient)

    def test_default_initialization(self):
        builder = ModbusBuilder()
        # Ensure all values are None by default
        self.assertIsNone(builder.coil_size)
        self.assertIsNone(builder.discrete_input_size)
        self.assertIsNone(builder.input_register_size)
        self.assertIsNone(builder.holding_register_size)
        self.assertIsNone(builder.timeout)
        self.assertIsNone(builder.retries)
        self.assertIsNone(builder.reconnect_delay)
        self.assertIsNone(builder.reconnect_delay_max)

    def test_builder_with_valid_values(self):
        builder = ModbusBuilder()
        builder.set_coil_size(CoilSize(10))
        builder.set_discrete_input_size(DiscreteInputSize(20))
        builder.set_input_register_size(InputRegisterSize(30))
        builder.set_holding_register_size(HoldingRegisterSize(40))
        builder.set_timeout(Timeout(5.0))
        builder.set_retries(Retries(5))
        builder.set_reconnect_delay(ReconnectDelay(2.0))
        builder.set_reconnect_delay_max(ReconnectDelayMax(10.0))

        self.assertEqual(builder.coil_size.value, 10)
        self.assertEqual(builder.discrete_input_size.value, 20)
        self.assertEqual(builder.input_register_size.value, 30)
        self.assertEqual(builder.holding_register_size.value, 40)
        self.assertEqual(builder.timeout.value, 5.0)
        self.assertEqual(builder.retries.value, 5)
        self.assertEqual(builder.reconnect_delay.value, 2.0)
        self.assertEqual(builder.reconnect_delay_max.value, 10.0)

    def test_builder_with_invalid_values(self):
        # Testing invalid values for each setter
        self.assertEqual(CoilSize(-1).status, Status.EXCEPTION)
        self.assertEqual(DiscreteInputSize(-1).status, Status.EXCEPTION)
        self.assertEqual(InputRegisterSize(-1).status, Status.EXCEPTION)
        self.assertEqual(HoldingRegisterSize(-1).status, Status.EXCEPTION)
        self.assertEqual(Timeout(-1).status, Status.EXCEPTION)
        self.assertEqual(Retries(-1).status, Status.EXCEPTION)
        self.assertEqual(ReconnectDelay(-1).status, Status.EXCEPTION)
        self.assertEqual(ReconnectDelayMax(-1).status, Status.EXCEPTION)

    def test_builder_with_edge_values(self):
        builder = ModbusBuilder()
        builder.set_coil_size(CoilSize(1))
        builder.set_coil_size(CoilSize(65535))  # Max allowable value
        self.assertEqual(builder.coil_size.value, 65535)

    # noinspection PyTypeChecker
    def test_builder_with_invalid_types(self):
        builder = ModbusBuilder()
        with self.assertRaises(AssertionError):
            builder.set_coil_size("InvalidType")  # Invalid type


    def test_builder_with_invalid_coil_size(self):
        invalid_coil_size = CoilSize(-1)
        self.assertEqual(invalid_coil_size.status, Status.EXCEPTION)

    def test_build_without_registering_client(self):
        # Test case when no client class is registered
        ModbusBuilder._client_class = None
        builder = ModbusBuilder()
        with self.assertRaises(AssertionError):
            builder.build()

if __name__ == '__main__':
    unittest.main()
