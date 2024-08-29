import unittest
from unittest.mock import MagicMock, patch
from modbus.modbus_factory import ModbusFactory
from modbus.modbus import ModbusMode
from modbus.modbus_builder import ModbusBuilder
from modbus.pymodbus.modbus_rtu import ModbusRTU
from modbus.pymodbus.modbus_tcp import ModbusTCP
from utils.tcp_values import IPAddress, Port
from utils.rtu_values import BaudRate, ParityType, StopBits, SerialPort
from utils.modbus_values import CoilSize, DiscreteInputSize, InputRegisterSize, HoldingRegisterSize, Timeout, Retries, \
    ReconnectDelay, ReconnectDelayMax


class TestModbusFactory(unittest.TestCase):

    def setUp(self):
        # Set up a valid ModbusBuilder instance with all required properties
        self.builder = ModbusBuilder() \
            .set_coil_size(CoilSize(10)) \
            .set_discrete_input_size(DiscreteInputSize(5)) \
            .set_input_register_size(InputRegisterSize(5)) \
            .set_holding_register_size(HoldingRegisterSize(5)) \
            .set_timeout(Timeout(3.0)) \
            .set_retries(Retries(3)) \
            .set_reconnect_delay(ReconnectDelay(0.1)) \
            .set_reconnect_delay_max(ReconnectDelayMax(300.0))

    @patch('modbus.modbus_factory.ModbusTCPBuilder')
    def test_create_modbus_tcp(self, mock_modbus_tcp_builder):
        """Test creating a ModbusTCP instance."""
        # Mock the TCP instance and the builder
        mock_tcp_instance = MagicMock(spec=ModbusTCP)
        mock_tcp_builder = mock_modbus_tcp_builder.return_value
        mock_tcp_builder.build.return_value = mock_tcp_instance

        # Call the factory method with TCP mode
        result = ModbusFactory.create_modbus(
            mode=ModbusMode.TCP,
            builder=self.builder,
            ip_address=IPAddress("192.168.1.1"),
            port=Port(502)
        )

        # Assert that the builder was used correctly
        mock_modbus_tcp_builder.assert_called_once_with(self.builder)
        mock_tcp_builder.set_ip_address.assert_called_once_with(IPAddress("192.168.1.1"))
        mock_tcp_builder.set_port.assert_called_once_with(Port(502))
        mock_tcp_builder.build.assert_called_once()

        # Assert that the result is the mock instance
        self.assertEqual(result, mock_tcp_instance)


    @patch('modbus.modbus_factory.ModbusRTUBuilder')
    def test_create_modbus_rtu(self, mock_modbus_rtu_builder):
        """Test creating a ModbusRTU instance."""
        # Mock the RTU instance and the builder
        mock_rtu_instance = MagicMock(spec=ModbusRTU)
        mock_rtu_builder = mock_modbus_rtu_builder.return_value
        mock_rtu_builder.build.return_value = mock_rtu_instance

        # Call the factory method with RTU mode
        result = ModbusFactory.create_modbus(
            mode=ModbusMode.RTU,
            builder=self.builder,
            baud_rate=BaudRate(9600),
            parity=ParityType.EVEN,
            stop_bits=StopBits(1),
            serial_port=SerialPort("COM1")
        )

        # Assert that the builder was used correctly
        mock_modbus_rtu_builder.assert_called_once_with(self.builder)
        mock_rtu_builder.set_baud_rate.assert_called_once_with(BaudRate(9600))
        mock_rtu_builder.set_parity.assert_called_once_with(ParityType.EVEN)
        mock_rtu_builder.set_stop_bits.assert_called_once_with(StopBits(1))
        mock_rtu_builder.set_serial_port.assert_called_once_with(SerialPort("COM1"))
        mock_rtu_builder.build.assert_called_once()

        # Assert that the result is the mock instance
        self.assertEqual(result, mock_rtu_instance)


    def test_create_modbus_invalid_mode(self):
        """Test that an unsupported mode raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            # noinspection PyTypeChecker
            ModbusFactory.create_modbus(
                mode="INVALID_MODE",
                builder=self.builder
            )
        self.assertEqual(str(context.exception), "Unsupported mode. Use ModbusMode.TCP or ModbusMode.RTU.")


if __name__ == '__main__':
    unittest.main()
