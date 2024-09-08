import unittest

from modbus.modbus_values import Retries, StrictRetries, ReconnectDelay, StrictReconnectDelay, ReconnectDelayMax, \
    StrictReconnectDelayMax, Timeout, StrictTimeout, ModbusSize, StrictModbusSize, CoilSize, StrictCoilSize, \
    DiscreteInputSize, StrictDiscreteInputSize, InputRegisterSize, StrictInputRegisterSize, HoldingRegisterSize, \
    StrictHoldingRegisterSize
from utils.status import Status

class TestModbusValues(unittest.TestCase):

    # Test for Retries
    def test_retries_valid(self):
        retries = Retries(5)
        self.assertEqual(retries.status, Status.OK)
        self.assertEqual(retries.value, 5)

    def test_retries_invalid(self):
        retries = Retries(15)
        self.assertEqual(retries.status, Status.EXCEPTION)
        self.assertIsNone(retries.value)

    def test_strict_retries_invalid(self):
        with self.assertRaises(ValueError):
            StrictRetries(15)

    # Test for ReconnectDelay
    def test_reconnect_delay_valid(self):
        reconnect_delay = ReconnectDelay(2.5)
        self.assertEqual(reconnect_delay.status, Status.OK)
        self.assertEqual(reconnect_delay.value, 2.5)

    def test_reconnect_delay_invalid(self):
        reconnect_delay = ReconnectDelay(0)
        self.assertEqual(reconnect_delay.status, Status.EXCEPTION)
        self.assertIsNone(reconnect_delay.value)

    def test_strict_reconnect_delay_invalid(self):
        with self.assertRaises(ValueError):
            StrictReconnectDelay(0)

    # Test for ReconnectDelayMax
    def test_reconnect_delay_max_valid(self):
        reconnect_delay_max = ReconnectDelayMax(100)
        self.assertEqual(reconnect_delay_max.status, Status.OK)
        self.assertEqual(reconnect_delay_max.value, 100)

    def test_reconnect_delay_max_invalid(self):
        reconnect_delay_max = ReconnectDelayMax(400)
        self.assertEqual(reconnect_delay_max.status, Status.EXCEPTION)
        self.assertIsNone(reconnect_delay_max.value)

    def test_strict_reconnect_delay_max_invalid(self):
        with self.assertRaises(ValueError):
            StrictReconnectDelayMax(400)

    # Test for Timeout
    def test_timeout_valid(self):
        timeout = Timeout(30)
        self.assertEqual(timeout.status, Status.OK)
        self.assertEqual(timeout.value, 30)

    def test_timeout_invalid(self):
        timeout = Timeout(70)
        self.assertEqual(timeout.status, Status.EXCEPTION)
        self.assertIsNone(timeout.value)

    def test_strict_timeout_invalid(self):
        with self.assertRaises(ValueError):
            StrictTimeout(70)

    # Test for ModbusSize
    def test_modbus_size_valid(self):
        modbus_size = ModbusSize(1024)
        self.assertEqual(modbus_size.status, Status.OK)
        self.assertEqual(modbus_size.value, 1024)

    def test_modbus_size_invalid(self):
        modbus_size = ModbusSize(70000)
        self.assertEqual(modbus_size.status, Status.EXCEPTION)
        self.assertIsNone(modbus_size.value)

    def test_strict_modbus_size_invalid(self):
        with self.assertRaises(ValueError):
            StrictModbusSize(70000)

    # Test for CoilSize
    def test_coil_size_valid(self):
        coil_size = CoilSize(512)
        self.assertEqual(coil_size.status, Status.OK)
        self.assertEqual(coil_size.value, 512)

    def test_coil_size_invalid(self):
        coil_size = CoilSize(70000)
        self.assertEqual(coil_size.status, Status.EXCEPTION)
        self.assertIsNone(coil_size.value)

    def test_strict_coil_size_invalid(self):
        with self.assertRaises(ValueError):
            StrictCoilSize(70000)

    # Test for DiscreteInputSize
    def test_discrete_input_size_valid(self):
        discrete_input_size = DiscreteInputSize(512)
        self.assertEqual(discrete_input_size.status, Status.OK)
        self.assertEqual(discrete_input_size.value, 512)

    def test_discrete_input_size_invalid(self):
        discrete_input_size = DiscreteInputSize(70000)
        self.assertEqual(discrete_input_size.status, Status.EXCEPTION)
        self.assertIsNone(discrete_input_size.value)

    def test_strict_discrete_input_size_invalid(self):
        with self.assertRaises(ValueError):
            StrictDiscreteInputSize(70000)

    # Test for InputRegisterSize
    def test_input_register_size_valid(self):
        input_register_size = InputRegisterSize(1024)
        self.assertEqual(input_register_size.status, Status.OK)
        self.assertEqual(input_register_size.value, 1024)

    def test_input_register_size_invalid(self):
        input_register_size = InputRegisterSize(70000)
        self.assertEqual(input_register_size.status, Status.EXCEPTION)
        self.assertIsNone(input_register_size.value)

    def test_strict_input_register_size_invalid(self):
        with self.assertRaises(ValueError):
            StrictInputRegisterSize(70000)

    # Test for HoldingRegisterSize
    def test_holding_register_size_valid(self):
        holding_register_size = HoldingRegisterSize(1024)
        self.assertEqual(holding_register_size.status, Status.OK)
        self.assertEqual(holding_register_size.value, 1024)

    def test_holding_register_size_invalid(self):
        holding_register_size = HoldingRegisterSize(70000)
        self.assertEqual(holding_register_size.status, Status.EXCEPTION)
        self.assertIsNone(holding_register_size.value)

    def test_strict_holding_register_size_invalid(self):
        with self.assertRaises(ValueError):
            StrictHoldingRegisterSize(70000)
