import unittest
from utils.modbus_values import Retries, ReconnectDelay, ReconnectDelayMax, Timeout, CoilSize, DiscreteInputSize, \
    InputRegisterSize, HoldingRegisterSize


class TestModbusValues(unittest.TestCase):

    def test_retries_valid(self):
        retries = Retries(3)
        self.assertEqual(retries.value, 3)

    def test_retries_invalid(self):
        with self.assertRaises(ValueError):
            Retries(-1)
        with self.assertRaises(ValueError):
            Retries(11)
        with self.assertRaises(ValueError):
            Retries(3.5)

    def test_reconnect_delay_valid(self):
        delay = ReconnectDelay(0.1)
        self.assertEqual(delay.value, 0.1)

        delay = ReconnectDelay(300.0)
        self.assertEqual(delay.value, 300.0)

    def test_reconnect_delay_invalid(self):
        with self.assertRaises(ValueError):
            ReconnectDelay(-0.1)
        with self.assertRaises(ValueError):
            ReconnectDelay(301)
        with self.assertRaises(ValueError):
            ReconnectDelay("invalid")

    def test_reconnect_delay_max_valid(self):
        delay_max = ReconnectDelayMax(0.1)
        self.assertEqual(delay_max.value, 0.1)

        delay_max = ReconnectDelayMax(300.0)
        self.assertEqual(delay_max.value, 300.0)

    def test_reconnect_delay_max_invalid(self):
        with self.assertRaises(ValueError):
            ReconnectDelayMax(-0.1)
        with self.assertRaises(ValueError):
            ReconnectDelayMax(301)
        with self.assertRaises(ValueError):
            ReconnectDelayMax("invalid")

    def test_timeout_valid(self):
        timeout = Timeout(1.0)
        self.assertEqual(timeout.value, 1.0)

        timeout = Timeout(60.0)
        self.assertEqual(timeout.value, 60.0)

    def test_timeout_invalid(self):
        with self.assertRaises(ValueError):
            Timeout(-0.1)
        with self.assertRaises(ValueError):
            Timeout(61)
        with self.assertRaises(ValueError):
            Timeout("invalid")

    # New tests for Modbus sizes

    def test_coil_size_valid(self):
        coil_size = CoilSize(1000)
        self.assertEqual(coil_size.value, 1000)

        coil_size = CoilSize(65535)
        self.assertEqual(coil_size.value, 65535)

    def test_coil_size_invalid(self):
        with self.assertRaises(ValueError):
            CoilSize(-1)
        with self.assertRaises(ValueError):
            CoilSize(65536)
        with self.assertRaises(ValueError):
            CoilSize("invalid")

    def test_discrete_input_size_valid(self):
        discrete_input_size = DiscreteInputSize(1000)
        self.assertEqual(discrete_input_size.value, 1000)

        discrete_input_size = DiscreteInputSize(65535)
        self.assertEqual(discrete_input_size.value, 65535)

    def test_discrete_input_size_invalid(self):
        with self.assertRaises(ValueError):
            DiscreteInputSize(-1)
        with self.assertRaises(ValueError):
            DiscreteInputSize(65536)
        with self.assertRaises(ValueError):
            DiscreteInputSize("invalid")

    def test_input_register_size_valid(self):
        input_register_size = InputRegisterSize(1000)
        self.assertEqual(input_register_size.value, 1000)

        input_register_size = InputRegisterSize(65535)
        self.assertEqual(input_register_size.value, 65535)

    def test_input_register_size_invalid(self):
        with self.assertRaises(ValueError):
            InputRegisterSize(-1)
        with self.assertRaises(ValueError):
            InputRegisterSize(65536)
        with self.assertRaises(ValueError):
            InputRegisterSize("invalid")

    def test_holding_register_size_valid(self):
        holding_register_size = HoldingRegisterSize(1000)
        self.assertEqual(holding_register_size.value, 1000)

        holding_register_size = HoldingRegisterSize(65535)
        self.assertEqual(holding_register_size.value, 65535)

    def test_holding_register_size_invalid(self):
        with self.assertRaises(ValueError):
            HoldingRegisterSize(-1)
        with self.assertRaises(ValueError):
            HoldingRegisterSize(65536)
        with self.assertRaises(ValueError):
            HoldingRegisterSize("invalid")

if __name__ == '__main__':
    unittest.main()
