import unittest
from unittest.mock import patch, MagicMock

from modbus.modus_rtu_builder import ModbusRTUBuilder
from modbus.rtu_values import BaudRate, StopBits, SerialPort, ParityType
from modbus.modbus_values import Timeout, Retries, ReconnectDelay, ReconnectDelayMax
from py_modbus.modbus_rtu import ModbusRTU


class TestModbusRTUBuilder(unittest.TestCase):

    def test_set_baud_rate(self):
        builder = ModbusRTUBuilder(client_class=ModbusRTU)
        baud_rate = BaudRate(9600)
        builder.set_baud_rate(baud_rate)
        self.assertEqual(builder.baud_rate, baud_rate)

    def test_set_parity(self):
        builder = ModbusRTUBuilder(client_class=ModbusRTU)
        parity = ParityType.EVEN
        builder.set_parity(parity)
        self.assertEqual(builder.parity, parity)

    def test_set_stop_bits(self):
        builder = ModbusRTUBuilder(client_class=ModbusRTU)
        stop_bits = StopBits(1)
        builder.set_stop_bits(stop_bits)
        self.assertEqual(builder.stop_bits, stop_bits)

    def test_set_serial_port(self):
        builder = ModbusRTUBuilder(client_class=ModbusRTU)
        serial_port = SerialPort("COM1")
        builder.set_serial_port(serial_port)
        self.assertEqual(builder.serial_port, serial_port)

    def test_build_valid(self):
        builder = ModbusRTUBuilder(client_class=ModbusRTU)
        builder.set_baud_rate(BaudRate(9600)) \
            .set_parity(ParityType.EVEN) \
            .set_stop_bits(StopBits(1)) \
            .set_serial_port(SerialPort("COM1")) \
            .set_timeout(Timeout(10)) \
            .set_reconnect_delay(ReconnectDelay(300)) \
            .set_reconnect_delay_max(ReconnectDelayMax(300)) \
            .set_retries(Retries(2))

        with patch('py_modbus.modbus_rtu.AsyncModbusSerialClient', new_callable=MagicMock) as mock_client:
            modbus_rtu = builder.build()
            self.assertIsInstance(modbus_rtu, ModbusRTU)
            self.assertTrue(mock_client.called)

    def test_build_without_baud_rate(self):
        builder = ModbusRTUBuilder(client_class=ModbusRTU)
        builder.set_parity(ParityType.EVEN) \
            .set_stop_bits(StopBits(1)) \
            .set_serial_port(SerialPort("COM1"))
        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_without_parity(self):
        builder = ModbusRTUBuilder(client_class=ModbusRTU)
        builder.set_baud_rate(BaudRate(9600)) \
            .set_stop_bits(StopBits(1)) \
            .set_serial_port(SerialPort("COM1"))
        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_without_stop_bits(self):
        builder = ModbusRTUBuilder(client_class=ModbusRTU)
        builder.set_baud_rate(BaudRate(9600)) \
            .set_parity(ParityType.EVEN) \
            .set_serial_port(SerialPort("COM1"))
        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_without_serial_port(self):
        builder = ModbusRTUBuilder(client_class=ModbusRTU)
        builder.set_baud_rate(BaudRate(9600)) \
            .set_parity(ParityType.EVEN) \
            .set_stop_bits(StopBits(1))
        with self.assertRaises(AssertionError):
            builder.build()

    def test_invalid_baud_rate(self):
        builder = ModbusRTUBuilder(client_class=ModbusRTU)
        with self.assertRaises(AssertionError):
            # noinspection PyTypeChecker
            builder.set_baud_rate("invalid_baud_rate")

    def test_invalid_parity(self):
        builder = ModbusRTUBuilder(client_class=ModbusRTU)
        with self.assertRaises(AssertionError):
            # noinspection PyTypeChecker
            builder.set_parity("invalid_parity")

    def test_invalid_stop_bits(self):
        builder = ModbusRTUBuilder(client_class=ModbusRTU)
        with self.assertRaises(AssertionError):
            # noinspection PyTypeChecker
            builder.set_stop_bits("invalid_stop_bits")

    def test_invalid_serial_port(self):
        builder = ModbusRTUBuilder(client_class=ModbusRTU)
        with self.assertRaises(AssertionError):
            # noinspection PyTypeChecker
            builder.set_serial_port("invalid_serial_port")

if __name__ == '__main__':
    unittest.main()
