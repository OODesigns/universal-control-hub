import unittest
from unittest.mock import patch, AsyncMock
from modbus.modus_rtu_builder import ModbusRTUBuilder
from modbus.pymodbus.modbus_rtu import ModbusRTU
from utils.rtu_values import BaudRate, StopBits, SerialPort, ParityType
from utils.modbus_values import Timeout, Retries, ReconnectDelay, ReconnectDelayMax

class TestModbusRTU(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Setting up a ModbusRTUBuilder with all necessary values
        self.builder = ModbusRTUBuilder()
        self.builder.set_baud_rate(BaudRate(9600)) \
            .set_parity(ParityType.EVEN) \
            .set_stop_bits(StopBits(1)) \
            .set_serial_port(SerialPort("COM1")) \
            .set_timeout(Timeout(5)) \
            .set_retries(Retries(3)) \
            .set_reconnect_delay(ReconnectDelay(0.1)) \
            .set_reconnect_delay_max(ReconnectDelayMax(10))

    @patch('modbus.pymodbus.modbus_rtu.AsyncModbusSerialClient')
    @patch('modbus.pymodbus.modus_client.ModbusConnectionManager')
    async def test_connect(self, mock_client_manager_cls, mock_client_cls):
        mock_client = AsyncMock()
        mock_client_cls.return_value = mock_client

        mock_client_manager = AsyncMock()
        mock_client_manager_cls.return_value = mock_client_manager

        # Instantiate ModbusRTU with the builder
        modbus_rtu = self.builder.build()

        # Perform the connect operation
        await modbus_rtu.connect()

        # Ensure the ModbusClientManager is initialized correctly
        mock_client_manager_cls.assert_called_once_with(mock_client)

        # Ensure connect is called on the client manager
        mock_client_manager.connect.assert_called_once()

        # Ensure the AsyncModbusSerialClient is instantiated with the correct parameters
        mock_client_cls.assert_called_once_with(
            port='COM1',
            baudrate=9600,
            parity=ParityType.EVEN.value,
            stopbits=1,
            timeout=5,
            reconnect_delay=0.1,
            reconnect_delay_max=10,
            retries=3
        )

    def test_invalid_builder_type(self):
        with self.assertRaises(AssertionError):
            # Pass an invalid builder type to the ModbusTCP constructor
            # noinspection PyTypeChecker
            ModbusRTU(builder="InvalidBuilderType")

if __name__ == '__main__':
    unittest.main()
