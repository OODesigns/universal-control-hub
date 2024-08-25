import unittest
from utils.modbus_values import (
    Retries, ReconnectDelay, ReconnectDelayMax, Timeout, CoilSize, DiscreteInputSize,
    InputRegisterSize, HoldingRegisterSize, StrictRetries, StrictReconnectDelay,
    StrictReconnectDelayMax, StrictTimeout, StrictCoilSize, StrictDiscreteInputSize,
    StrictInputRegisterSize, StrictHoldingRegisterSize
)
from utils.value import ValueStatus

class TestModbusValues(unittest.TestCase):

    def test_retries_valid(self):
        retries = Retries(3)
        self.assertEqual(retries.value, 3)
        self.assertEqual(retries.status, ValueStatus.OK)

    def test_retries_invalid(self):
        retries = Retries(-1)
        self.assertEqual(retries.status, ValueStatus.EXCEPTION)
        with self.assertRaises(ValueError):
            _ = retries.value

    def test_strict_retries_invalid(self):
        with self.assertRaises(ValueError):
            StrictRetries(-1)

    def test_reconnect_delay_valid(self):
        delay = ReconnectDelay(0.1)
        self.assertEqual(delay.value, 0.1)
        self.assertEqual(delay.status, ValueStatus.OK)

    def test_reconnect_delay_invalid(self):
        delay = ReconnectDelay(-0.1)
        self.assertEqual(delay.status, ValueStatus.EXCEPTION)
        with self.assertRaises(ValueError):
            _ = delay.value

    def test_strict_reconnect_delay_invalid(self):
        with self.assertRaises(ValueError):
            StrictReconnectDelay(-0.1)

    def test_reconnect_delay_max_valid(self):
        delay_max = ReconnectDelayMax(0.1)
        self.assertEqual(delay_max.value, 0.1)
        self.assertEqual(delay_max.status, ValueStatus.OK)

    def test_reconnect_delay_max_invalid(self):
        delay_max = ReconnectDelayMax(301)
        self.assertEqual(delay_max.status, ValueStatus.EXCEPTION)
        with self.assertRaises(ValueError):
            _ = delay_max.value

    def test_strict_reconnect_delay_max_invalid(self):
        with self.assertRaises(ValueError):
            StrictReconnectDelayMax(301)

    def test_timeout_valid(self):
        timeout = Timeout(1.0)
        self.assertEqual(timeout.value, 1.0)
        self.assertEqual(timeout.status, ValueStatus.OK)

    def test_timeout_invalid(self):
        timeout = Timeout(-0.1)
        self.assertEqual(timeout.status, ValueStatus.EXCEPTION)
        with self.assertRaises(ValueError):
            _ = timeout.value

    def test_strict_timeout_invalid(self):
        with self.assertRaises(ValueError):
            StrictTimeout(-0.1)

    def test_coil_size_valid(self):
        coil_size = CoilSize(1000)
        self.assertEqual(coil_size.value, 1000)
        self.assertEqual(coil_size.status, ValueStatus.OK)

    def test_coil_size_invalid(self):
        coil_size = CoilSize(-1)
        self.assertEqual(coil_size.status, ValueStatus.EXCEPTION)
        with self.assertRaises(ValueError):
            _ = coil_size.value

    def test_strict_coil_size_invalid(self):
        with self.assertRaises(ValueError):
            StrictCoilSize(-1)

    def test_discrete_input_size_valid(self):
        discrete_input_size = DiscreteInputSize(1000)
        self.assertEqual(discrete_input_size.value, 1000)
        self.assertEqual(discrete_input_size.status, ValueStatus.OK)

    def test_discrete_input_size_invalid(self):
        discrete_input_size = DiscreteInputSize(-1)
        self.assertEqual(discrete_input_size.status, ValueStatus.EXCEPTION)
        with self.assertRaises(ValueError):
            _ = discrete_input_size.value

    def test_strict_discrete_input_size_invalid(self):
        with self.assertRaises(ValueError):
            StrictDiscreteInputSize(-1)

    def test_input_register_size_valid(self):
        input_register_size = InputRegisterSize(1000)
        self.assertEqual(input_register_size.value, 1000)
        self.assertEqual(input_register_size.status, ValueStatus.OK)

    def test_input_register_size_invalid(self):
        input_register_size = InputRegisterSize(-1)
        self.assertEqual(input_register_size.status, ValueStatus.EXCEPTION)
        with self.assertRaises(ValueError):
            _ = input_register_size.value

    def test_strict_input_register_size_invalid(self):
        with self.assertRaises(ValueError):
            StrictInputRegisterSize(-1)

    def test_holding_register_size_valid(self):
        holding_register_size = HoldingRegisterSize(1000)
        self.assertEqual(holding_register_size.value, 1000)
        self.assertEqual(holding_register_size.status, ValueStatus.OK)

    def test_holding_register_size_invalid(self):
        holding_register_size = HoldingRegisterSize(-1)
        self.assertEqual(holding_register_size.status, ValueStatus.EXCEPTION)
        with self.assertRaises(ValueError):
            _ = holding_register_size.value

    def test_strict_holding_register_size_invalid(self):
        with self.assertRaises(ValueError):
            StrictHoldingRegisterSize(-1)

if __name__ == '__main__':
    unittest.main()
