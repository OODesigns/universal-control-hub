import unittest
import utils.modbus_values


class TestModbusValues(unittest.TestCase):

    def test_retries_valid(self):
        retries = utils.modbus_values.Retries(3)
        self.assertEqual(retries.value, 3)

    def test_retries_invalid(self):
        with self.assertRaises(ValueError):
            utils.modbus_values.Retries(-1)
        with self.assertRaises(ValueError):
            utils.modbus_values.Retries(11)
        with self.assertRaises(ValueError):
            utils.modbus_values.Retries(3.5)

    def test_reconnect_delay_valid(self):
        delay = utils.modbus_values.ReconnectDelay(0.1)
        self.assertEqual(delay.value, 0.1)

        delay = utils.modbus_values.ReconnectDelay(300.0)
        self.assertEqual(delay.value, 300.0)

    def test_reconnect_delay_invalid(self):
        with self.assertRaises(ValueError):
            utils.modbus_values.ReconnectDelay(-0.1)
        with self.assertRaises(ValueError):
            utils.modbus_values.ReconnectDelay(301)
        with self.assertRaises(ValueError):
            utils.modbus_values.ReconnectDelay("invalid")

    def test_reconnect_delay_max_valid(self):
        delay_max = utils.modbus_values.ReconnectDelayMax(0.1)
        self.assertEqual(delay_max.value, 0.1)

        delay_max = utils.modbus_values.ReconnectDelayMax(300.0)
        self.assertEqual(delay_max.value, 300.0)

    def test_reconnect_delay_max_invalid(self):
        with self.assertRaises(ValueError):
            utils.modbus_values.ReconnectDelayMax(-0.1)
        with self.assertRaises(ValueError):
            utils.modbus_values.ReconnectDelayMax(301)
        with self.assertRaises(ValueError):
            utils.modbus_values.ReconnectDelayMax("invalid")

    def test_timeout_valid(self):
        timeout = utils.modbus_values.Timeout(1.0)
        self.assertEqual(timeout.value, 1.0)

        timeout = utils.modbus_values.Timeout(60.0)
        self.assertEqual(timeout.value, 60.0)

    def test_timeout_invalid(self):
        with self.assertRaises(ValueError):
            utils.modbus_values.Timeout(-0.1)
        with self.assertRaises(ValueError):
            utils.modbus_values.Timeout(61)
        with self.assertRaises(ValueError):
            utils.modbus_values.Timeout("invalid")

    # New tests for Modbus sizes

    def test_coil_size_valid(self):
        coil_size = utils.modbus_values.CoilSize(1000)
        self.assertEqual(coil_size.value, 1000)

        coil_size = utils.modbus_values.CoilSize(65535)
        self.assertEqual(coil_size.value, 65535)

    def test_coil_size_invalid(self):
        with self.assertRaises(ValueError):
            utils.modbus_values.CoilSize(-1)
        with self.assertRaises(ValueError):
            utils.modbus_values.CoilSize(65536)
        with self.assertRaises(ValueError):
            utils.modbus_values.CoilSize("invalid")

    def test_discrete_input_size_valid(self):
        discrete_input_size = utils.modbus_values.DiscreteInputSize(1000)
        self.assertEqual(discrete_input_size.value, 1000)

        discrete_input_size = utils.modbus_values.DiscreteInputSize(65535)
        self.assertEqual(discrete_input_size.value, 65535)

    def test_discrete_input_size_invalid(self):
        with self.assertRaises(ValueError):
            utils.modbus_values.DiscreteInputSize(-1)
        with self.assertRaises(ValueError):
            utils.modbus_values.DiscreteInputSize(65536)
        with self.assertRaises(ValueError):
            utils.modbus_values.DiscreteInputSize("invalid")

    def test_input_register_size_valid(self):
        input_register_size = utils.modbus_values.InputRegisterSize(1000)
        self.assertEqual(input_register_size.value, 1000)

        input_register_size = utils.modbus_values.InputRegisterSize(65535)
        self.assertEqual(input_register_size.value, 65535)

    def test_input_register_size_invalid(self):
        with self.assertRaises(ValueError):
            utils.modbus_values.InputRegisterSize(-1)
        with self.assertRaises(ValueError):
            utils.modbus_values.InputRegisterSize(65536)
        with self.assertRaises(ValueError):
            utils.modbus_values.InputRegisterSize("invalid")

    def test_holding_register_size_valid(self):
        holding_register_size = utils.modbus_values.HoldingRegisterSize(1000)
        self.assertEqual(holding_register_size.value, 1000)

        holding_register_size = utils.modbus_values.HoldingRegisterSize(65535)
        self.assertEqual(holding_register_size.value, 65535)

    def test_holding_register_size_invalid(self):
        with self.assertRaises(ValueError):
            utils.modbus_values.HoldingRegisterSize(-1)
        with self.assertRaises(ValueError):
            utils.modbus_values.HoldingRegisterSize(65536)
        with self.assertRaises(ValueError):
            utils.modbus_values.HoldingRegisterSize("invalid")

if __name__ == '__main__':
    unittest.main()
