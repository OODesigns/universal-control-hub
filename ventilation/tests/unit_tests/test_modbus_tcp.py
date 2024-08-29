import unittest
from unittest.mock import patch, AsyncMock

from modbus.modbus_tcp_builder import ModbusTCPBuilder
from utils.tcp_values import IPAddress, Port
from utils.modbus_values import Timeout, Retries, ReconnectDelay, ReconnectDelayMax

class TestModbusTCP(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Setting up a ModbusTCPBuilder with all necessary values
        self.builder = ModbusTCPBuilder()
        self.builder.set_ip_address(IPAddress('192.168.1.100')) \
            .set_port(Port(502)) \
            .set_timeout(Timeout(5)) \
            .set_retries(Retries(3)) \
            .set_reconnect_delay(ReconnectDelay(0.1)) \
            .set_reconnect_delay_max(ReconnectDelayMax(10))

    @patch('modbus.pymodbus.modbus_tcp.AsyncModbusTcpClient')
    @patch('modbus.pymodbus.modus_base.ModbusClientManager')
    async def test_connect(self, mock_client_manager_cls, mock_client_cls):
        mock_client = AsyncMock()
        mock_client_cls.return_value = mock_client

        mock_client_manager = AsyncMock()
        mock_client_manager_cls.return_value = mock_client_manager

        # Instantiate ModbusTCP with the builder
        modbus_tcp = self.builder.build()

        # Perform the connect operation
        await modbus_tcp.connect()

        # Ensure the ModbusClientManager is initialized correctly
        mock_client_manager_cls.assert_called_once_with(mock_client)

        # Ensure connect is called on the client manager
        mock_client_manager.connect.assert_called_once()

        # Ensure the AsyncModbusTcpClient is instantiated with the correct parameters
        mock_client_cls.assert_called_once_with(
            host='192.168.1.100',
            port=502,
            timeout=5,
            reconnect_delay=0.1,
            reconnect_delay_max=10,
            retries=3
        )

if __name__ == '__main__':
    unittest.main()
