import unittest

from modbus.modbus_builder import ModbusBuilder
import utils.modbus_values

class TestModbusBuilder(unittest.TestCase):

    def test_builder_with_valid_values(self):
        builder = ModbusBuilder()
        builder.set_coil_size(utils.modbus_values.CoilSize(10))
        builder.set_discrete_input_size(utils.modbus_values.DiscreteInputSize(20))
        builder.set_input_register_size(utils.modbus_values.InputRegisterSize(30))
        builder.set_holding_register_size(utils.modbus_values.HoldingRegisterSize(40))
        builder.set_timeout(utils.modbus_values.Timeout(5.0))
        builder.set_retries(utils.modbus_values.Retries(5))
        builder.set_reconnect_delay(utils.modbus_values.ReconnectDelay(2.0))
        builder.set_reconnect_delay_max(utils.modbus_values.ReconnectDelayMax(10.0))

        self.assertEqual(builder.coil_size.value, 10)
        self.assertEqual(builder.discrete_input_size.value, 20)
        self.assertEqual(builder.input_register_size.value, 30)
        self.assertEqual(builder.holding_register_size.value, 40)
        self.assertEqual(builder.timeout.value, 5.0)
        self.assertEqual(builder.retries.value, 5)
        self.assertEqual(builder.reconnect_delay.value, 2.0)
        self.assertEqual(builder.reconnect_delay_max.value, 10.0)

    def test_builder_with_invalid_coil_size(self):
        builder = ModbusBuilder()
        with self.assertRaises(ValueError):
            builder.set_coil_size(utils.modbus_values.CoilSize(-1))  # Invalid negative coil size

    def test_builder_with_invalid_discrete_input_size(self):
        builder = ModbusBuilder()
        with self.assertRaises(ValueError):
            builder.set_discrete_input_size(utils.modbus_values.DiscreteInputSize(-1))  # Invalid negative discrete input size

    def test_builder_with_invalid_input_register_size(self):
        builder = ModbusBuilder()
        with self.assertRaises(ValueError):
            builder.set_input_register_size(utils.modbus_values.InputRegisterSize(-1))  # Invalid negative input register size

    def test_builder_with_invalid_holding_register_size(self):
        builder = ModbusBuilder()
        with self.assertRaises(ValueError):
            builder.set_holding_register_size(utils.modbus_values.HoldingRegisterSize(-1))  # Invalid negative holding register size

    def test_builder_with_invalid_timeout(self):
        builder = ModbusBuilder()
        with self.assertRaises(ValueError):
            builder.set_timeout(utils.modbus_values.Timeout(-1))  # Invalid negative timeout

    def test_builder_with_invalid_retries(self):
        builder = ModbusBuilder()
        with self.assertRaises(ValueError):
            builder.set_retries(utils.modbus_values.Retries(-1))  # Invalid negative retries

    def test_builder_with_invalid_reconnect_delay(self):
        builder = ModbusBuilder()
        with self.assertRaises(ValueError):
            builder.set_reconnect_delay(utils.modbus_values.ReconnectDelay(-1))  # Invalid negative reconnect delay

    def test_builder_with_invalid_reconnect_delay_max(self):
        builder = ModbusBuilder()
        with self.assertRaises(ValueError):
            builder.set_reconnect_delay_max(utils.modbus_values.ReconnectDelayMax(-1))  # Invalid negative reconnect delay max

    def test_copy_constructor_with_valid_builder(self):
        original_builder = ModbusBuilder()
        original_builder.set_coil_size(utils.modbus_values.CoilSize(10))
        original_builder.set_discrete_input_size(utils.modbus_values.DiscreteInputSize(20))
        original_builder.set_input_register_size(utils.modbus_values.InputRegisterSize(30))
        original_builder.set_holding_register_size(utils.modbus_values.HoldingRegisterSize(40))
        original_builder.set_timeout(utils.modbus_values.Timeout(5.0))
        original_builder.set_retries(utils.modbus_values.Retries(5))
        original_builder.set_reconnect_delay(utils.modbus_values.ReconnectDelay(2.0))
        original_builder.set_reconnect_delay_max(utils.modbus_values.ReconnectDelayMax(10.0))

        # Create a copy using the copy constructor
        copied_builder = ModbusBuilder(original_builder)

        # Ensure that the copied builder has the same values as the original
        self.assertEqual(copied_builder.coil_size.value, 10)
        self.assertEqual(copied_builder.discrete_input_size.value, 20)
        self.assertEqual(copied_builder.input_register_size.value, 30)
        self.assertEqual(copied_builder.holding_register_size.value, 40)
        self.assertEqual(copied_builder.timeout.value, 5.0)
        self.assertEqual(copied_builder.retries.value, 5)
        self.assertEqual(copied_builder.reconnect_delay.value, 2.0)
        self.assertEqual(copied_builder.reconnect_delay_max.value, 10.0)

    def test_copy_constructor_with_invalid_type(self):
        with self.assertRaises(TypeError):
            ModbusBuilder("invalid_builder")  # Pass an invalid type, should raise TypeError

    def test_copy_constructor_expecting_ModbusBuilder_to_be_complete(self):
        original_builder = ModbusBuilder()
        original_builder.set_coil_size(utils.modbus_values.CoilSize(10))

        with self.assertRaises(ValueError):
            ModbusBuilder(original_builder)


if __name__ == '__main__':
    unittest.main()
