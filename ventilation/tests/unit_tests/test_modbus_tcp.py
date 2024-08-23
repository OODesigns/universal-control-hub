import unittest
from unittest.mock import patch, AsyncMock
from utils.tcp_values import IPAddress, Port
from utils.modbus_values import Timeout, Retries, ReconnectDelay, ReconnectDelayMax
from devices.modbus_tcp_builder import ModbusTCPBuilder

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
        self.modbus_tcp = self.builder.build()

    @patch('devices.modbus_tcp.AsyncModbusTcpClient')
    async def test_connect(self, mock_client_cls):
        mock_client = AsyncMock()
        mock_client_cls.return_value = mock_client

        await self.modbus_tcp.connect()

        mock_client_cls.assert_called_once_with(
            host='192.168.1.100',
            port=502,
            timeout=5,
            reconnect_delay=0.1,
            reconnect_delay_max=10,
            retries=3
        )
        mock_client.connect.assert_called_once()



if __name__ == '__main__':
    unittest.main()
