import unittest
from unittest.mock import MagicMock, AsyncMock
from config.config_loader import ConfigLoader
from devices.mvhr import MVHR
from modbus.modbus import ModbusInterface
from modbus.modbus_builder import ModbusBuilder
from modbus.modbus_factory import ModbusFactory


class TestMVHRAsync(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Mock the ConfigLoader and ModbusFactory
        self.config_loader = MagicMock(spec=ConfigLoader)
        self.modbus_factory = MagicMock(spec=ModbusFactory)

        # Create a basic ModbusBuilder instance
        self.modbus_builder = ModbusBuilder()

        # Define a simple subclass for testing
        class TestMVHR(MVHR):
            def __init__(self, config_loader: ConfigLoader, modbus_factory: ModbusFactory, builder: ModbusBuilder):
                super().__init__(config_loader, modbus_factory)
                self.mock_modbus_interface = AsyncMock(spec=ModbusInterface)

            @property
            def modbus(self) -> ModbusInterface:
                return self.mock_modbus_interface

            async def read_data(self):
                pass

        # Instantiate the test MVHR class
        self.mvhr = TestMVHR(self.config_loader, self.modbus_factory, self.modbus_builder)

    async def test_start_connects_modbus(self):
        """Test that the ModbusInterface connect method is called on start."""
        await self.mvhr.start()
        self.mvhr.modbus.connect.assert_called_once()

    def test_stop_disconnects_modbus(self):
        """Test that the ModbusInterface disconnect method is called on stop."""
        self.mvhr.stop()
        self.mvhr.modbus.disconnect.assert_called_once()

if __name__ == '__main__':
    unittest.main()
