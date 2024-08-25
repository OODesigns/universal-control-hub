import unittest
from unittest.mock import patch, AsyncMock

from modbus.modbus_rtu import ParityType
from modbus.modus_rtu_builder import ModbusRTUBuilder
from utils.rtu_values import BaudRate, StopBits, SerialPort
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
        self.modbus_rtu = self.builder.build()

    @patch('devices.modbus_rtu.AsyncModbusSerialClient')
    async def test_connect(self, mock_client_cls):
        mock_client = AsyncMock()
        mock_client_cls.return_value = mock_client

        await self.modbus_rtu.connect()

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
        mock_client.connect.assert_called_once()

if __name__ == '__main__':
    unittest.main()
