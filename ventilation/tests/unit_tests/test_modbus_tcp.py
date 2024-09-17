import unittest
from unittest.mock import patch, AsyncMock, Mock

from modbus.modbus_tcp_client_builder import ModbusTCPClientBuilder
from modbus.tcp_values import IPAddress, Port
from modbus.modbus_values import Timeout, Retries, ReconnectDelay, ReconnectDelayMax
from py_modbus.modbus_tcp_client import ModbusTCPClient


class TestModbusTCP(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Setting up a ModbusTCPBuilder with all necessary values
        self.builder = ModbusTCPClientBuilder()
        self.builder.set_ip_address(IPAddress('192.168.1.100')) \
            .set_port(Port(502)) \
            .set_timeout(Timeout(5)) \
            .set_retries(Retries(3)) \
            .set_reconnect_delay(ReconnectDelay(0.1)) \
            .set_reconnect_delay_max(ReconnectDelayMax(10))

    @patch('py_modbus.modbus_tcp.AsyncModbusTcpClient')
    async def test_modbus_tcp_initialization(self, mock_async_client):
        # Mock the async client to avoid actual network calls
        mock_client_instance = AsyncMock()
        mock_async_client.return_value = mock_client_instance

        # Instantiate ModbusTCP with the builder
        modbus_tcp = ModbusTCPClient(self.builder)

        # Ensure that the AsyncModbusTcpClient is initialized with the correct parameters
        mock_async_client.assert_called_once_with(
            host='192.168.1.100',
            port=502,
            timeout=5,
            reconnect_delay=0.1,
            reconnect_delay_max=10,
            retries=3
        )
        self.assertIsInstance(modbus_tcp, ModbusTCPClient)

    @patch('py_modbus.modbus_tcp.AsyncModbusTcpClient')
    async def test_connect(self, mock_async_client):
        mock_client_instance = AsyncMock()
        mock_async_client.return_value = mock_client_instance

        modbus_tcp = ModbusTCPClient(self.builder)
        await modbus_tcp.connect()

        # Ensure the connect method is called on the mock client
        mock_client_instance.connect.assert_called_once()

    @patch('py_modbus.modbus_tcp.AsyncModbusTcpClient')
    async def test_disconnect(self, mock_async_client):
        mock_client_instance = Mock()
        mock_async_client.return_value = mock_client_instance

        modbus_tcp = ModbusTCPClient(self.builder)
        modbus_tcp.disconnect()

        # Ensure the disconnect method is called on the mock client
        mock_client_instance.close.assert_called_once()

    def test_invalid_builder_type(self):
        with self.assertRaises(AssertionError):
            # Pass an invalid builder type to the ModbusTCP constructor
            # noinspection PyTypeChecker
            ModbusTCPClient(builder="InvalidBuilderType")

if __name__ == '__main__':
    unittest.main()
