import unittest
from modbus.modbus_builder import ModbusBuilder
import modbus.modbus_values
from utils.status import Status


class TestModbusBuilder(unittest.TestCase):

    def test_builder_with_valid_values(self):
        builder = ModbusBuilder()
        builder.set_coil_size(modbus.modbus_values.CoilSize(10))
        builder.set_discrete_input_size(modbus.modbus_values.DiscreteInputSize(20))
        builder.set_input_register_size(modbus.modbus_values.InputRegisterSize(30))
        builder.set_holding_register_size(modbus.modbus_values.HoldingRegisterSize(40))
        builder.set_timeout(modbus.modbus_values.Timeout(5.0))
        builder.set_retries(modbus.modbus_values.Retries(5))
        builder.set_reconnect_delay(modbus.modbus_values.ReconnectDelay(2.0))
        builder.set_reconnect_delay_max(modbus.modbus_values.ReconnectDelayMax(10.0))

        self.assertEqual(builder.coil_size.value, 10)
        self.assertEqual(builder.discrete_input_size.value, 20)
        self.assertEqual(builder.input_register_size.value, 30)
        self.assertEqual(builder.holding_register_size.value, 40)
        self.assertEqual(builder.timeout.value, 5.0)
        self.assertEqual(builder.retries.value, 5)
        self.assertEqual(builder.reconnect_delay.value, 2.0)
        self.assertEqual(builder.reconnect_delay_max.value, 10.0)

    def test_builder_with_invalid_coil_size(self):
        invalid_coil_size = modbus.modbus_values.CoilSize(-1)
        self.assertEqual(invalid_coil_size.status, Status.EXCEPTION)

    def test_builder_with_invalid_discrete_input_size(self):
        invalid_discrete_input_size = modbus.modbus_values.DiscreteInputSize(-1)
        self.assertEqual(invalid_discrete_input_size.status, Status.EXCEPTION)

    def test_builder_with_invalid_input_register_size(self):
        invalid_input_register_size = modbus.modbus_values.InputRegisterSize(-1)
        self.assertEqual(invalid_input_register_size.status, Status.EXCEPTION)

    def test_builder_with_invalid_holding_register_size(self):
        invalid_holding_register_size = modbus.modbus_values.HoldingRegisterSize(-1)
        self.assertEqual(invalid_holding_register_size.status, Status.EXCEPTION)

    def test_builder_with_invalid_timeout(self):
        invalid_timeout = modbus.modbus_values.Timeout(-1)
        self.assertEqual(invalid_timeout.status, Status.EXCEPTION)

    def test_builder_with_invalid_retries(self):
        invalid_retries = modbus.modbus_values.Retries(-1)
        self.assertEqual(invalid_retries.status, Status.EXCEPTION)

    def test_builder_with_invalid_reconnect_delay(self):
        invalid_reconnect_delay = modbus.modbus_values.ReconnectDelay(-1)
        self.assertEqual(invalid_reconnect_delay.status, Status.EXCEPTION)

    def test_builder_with_invalid_reconnect_delay_max(self):
        invalid_reconnect_delay_max = modbus.modbus_values.ReconnectDelayMax(-1)
        self.assertEqual(invalid_reconnect_delay_max.status, Status.EXCEPTION)

    def test_copy_constructor_with_valid_builder(self):
        original_builder = ModbusBuilder()
        original_builder.set_coil_size(modbus.modbus_values.CoilSize(10))
        original_builder.set_discrete_input_size(modbus.modbus_values.DiscreteInputSize(20))
        original_builder.set_input_register_size(modbus.modbus_values.InputRegisterSize(30))
        original_builder.set_holding_register_size(modbus.modbus_values.HoldingRegisterSize(40))
        original_builder.set_timeout(modbus.modbus_values.Timeout(5.0))
        original_builder.set_retries(modbus.modbus_values.Retries(5))
        original_builder.set_reconnect_delay(modbus.modbus_values.ReconnectDelay(2.0))
        original_builder.set_reconnect_delay_max(modbus.modbus_values.ReconnectDelayMax(10.0))

        copied_builder = ModbusBuilder(original_builder)

        self.assertEqual(copied_builder.coil_size.value, 10)
        self.assertEqual(copied_builder.discrete_input_size.value, 20)
        self.assertEqual(copied_builder.input_register_size.value, 30)
        self.assertEqual(copied_builder.holding_register_size.value, 40)
        self.assertEqual(copied_builder.timeout.value, 5.0)
        self.assertEqual(copied_builder.retries.value, 5)
        self.assertEqual(copied_builder.reconnect_delay.value, 2.0)
        self.assertEqual(copied_builder.reconnect_delay_max.value, 10.0)

    def test_copy_constructor_with_invalid_type(self):
        with self.assertRaises(AssertionError):
            ModbusBuilder("invalid_builder")

    def test_builder_with_edge_values(self):
        builder = ModbusBuilder()
        builder.set_coil_size(modbus.modbus_values.CoilSize(1))
        builder.set_coil_size(modbus.modbus_values.CoilSize(65535))
        self.assertEqual(builder.coil_size.value, 65535)

    def test_builder_with_invalid_types(self):
        builder = ModbusBuilder()
        with self.assertRaises(AssertionError):
            # noinspection PyTypeChecker
            builder.set_coil_size("InvalidType")

    def test_default_initialization(self):
        builder = ModbusBuilder()
        self.assertIsNone(builder.coil_size)
        self.assertIsNone(builder.discrete_input_size)
        self.assertIsNone(builder.input_register_size)
        self.assertIsNone(builder.holding_register_size)
        self.assertIsNone(builder.timeout)
        self.assertIsNone(builder.retries)
        self.assertIsNone(builder.reconnect_delay)
        self.assertIsNone(builder.reconnect_delay_max)

if __name__ == '__main__':
    unittest.main()
