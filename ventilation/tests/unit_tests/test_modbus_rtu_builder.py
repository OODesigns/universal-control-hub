import unittest
from unittest.mock import patch
from modbus.modus_rtu_builder import ModbusRTUBuilder
from utils.modbus_values import Timeout, ReconnectDelay, ReconnectDelayMax, Retries
from utils.rtu_values import BaudRate, StopBits, SerialPort, ParityType


class TestModbusRTUBuilder(unittest.TestCase):

    def test_set_baud_rate(self):
        builder = ModbusRTUBuilder()
        baud_rate = BaudRate(9600)
        builder.set_baud_rate(baud_rate)
        self.assertEqual(builder.baud_rate, baud_rate)

    def test_set_parity(self):
        builder = ModbusRTUBuilder()
        parity = ParityType.EVEN
        builder.set_parity(parity)
        self.assertEqual(builder.parity, parity)

    def test_set_stop_bits(self):
        builder = ModbusRTUBuilder()
        stop_bits = StopBits(1)
        builder.set_stop_bits(stop_bits)
        self.assertEqual(builder.stop_bits, stop_bits)

    def test_set_serial_port(self):
        builder = ModbusRTUBuilder()
        serial_port = SerialPort("COM1")
        builder.set_serial_port(serial_port)
        self.assertEqual(builder.serial_port, serial_port)

    def test_build_valid(self):
        builder = ModbusRTUBuilder()
        builder.set_baud_rate(BaudRate(9600)) \
            .set_parity(ParityType.EVEN) \
            .set_stop_bits(StopBits(1)) \
            .set_serial_port(SerialPort("COM1")) \
            .set_timeout(Timeout(10)) \
            .set_reconnect_delay(ReconnectDelay(300)) \
            .set_reconnect_delay_max(ReconnectDelayMax(300)) \
            .set_retries(Retries(2))

        # patch it where it's used, not where it's defined.
        with patch('modbus.modus_rtu_builder.ModbusRTU') as MockModbusRTU:
            mock_instance = MockModbusRTU.return_value
            modbus_rtu = builder.build()
            self.assertIs(modbus_rtu, mock_instance)

    def test_build_without_baud_rate(self):
        builder = ModbusRTUBuilder()
        builder.set_parity(ParityType.EVEN) \
            .set_stop_bits(StopBits(1)) \
            .set_serial_port(SerialPort("COM1"))
        with self.assertRaises(ValueError):
            builder.build()

    def test_build_without_parity(self):
        builder = ModbusRTUBuilder()
        builder.set_baud_rate(BaudRate(9600)) \
            .set_stop_bits(StopBits(1)) \
            .set_serial_port(SerialPort("COM1"))
        with self.assertRaises(ValueError):
            builder.build()

    def test_build_without_stop_bits(self):
        builder = ModbusRTUBuilder()
        builder.set_baud_rate(BaudRate(9600)) \
            .set_parity(ParityType.EVEN) \
            .set_serial_port(SerialPort("COM1"))
        with self.assertRaises(ValueError):
            builder.build()

    def test_build_without_serial_port(self):
        builder = ModbusRTUBuilder()
        builder.set_baud_rate(BaudRate(9600)) \
            .set_parity(ParityType.EVEN) \
            .set_stop_bits(StopBits(1))
        with self.assertRaises(ValueError):
            builder.build()

    def test_invalid_baud_rate(self):
        builder = ModbusRTUBuilder()
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            builder.set_baud_rate("invalid_baud_rate")

    def test_invalid_parity(self):
        builder = ModbusRTUBuilder()
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            builder.set_parity("invalid_parity")

    def test_invalid_stop_bits(self):
        builder = ModbusRTUBuilder()
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            builder.set_stop_bits("invalid_stop_bits")

    def test_invalid_serial_port(self):
        builder = ModbusRTUBuilder()
        with self.assertRaises(ValueError):
            # noinspection PyTypeChecker
            builder.set_serial_port("invalid_serial_port")

if __name__ == '__main__':
    unittest.main()
