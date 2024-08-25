import unittest
from unittest.mock import MagicMock, AsyncMock
from config.config_loader import ConfigLoader
from devices.mvhr import MVHR, MVHR_RUNNING, MVHR_START_FAILURE
from modbus.modbus import ModbusInterface, ModbusMode
from modbus.modbus_builder import ModbusBuilder
from modbus.modbus_factory import ModbusFactory
from state.state_manager import StateManager
import utils.modbus_values
from utils.tcp_values import IPAddress, Port

class TestMVHRAsync(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Mock the ConfigLoader to avoid needing a real config file
        self.config_loader = MagicMock(spec=ConfigLoader)
        self.config_loader.get_value.side_effect = lambda key: {
            'mvhr-timeout': 10,
            'mvhr-port': 502,
            'mvhr-ip-address': '192.168.0.100'
        }[key]

        # Set up the state manager and mock modbus
        self.state_manager = MagicMock(spec=StateManager)
        self.mock_modbus_interface = AsyncMock(spec=ModbusInterface)
        self.modbus_factory = MagicMock(spec=ModbusFactory)

        # Create a ModbusBuilder with specific size objects
        self.modbus_builder = ModbusBuilder()
        self.modbus_builder.set_coil_size(utils.modbus_values.CoilSize(10))
        self.modbus_builder.set_discrete_input_size(utils.modbus_values.DiscreteInputSize(5))
        self.modbus_builder.set_input_register_size(utils.modbus_values.InputRegisterSize(5))
        self.modbus_builder.set_holding_register_size(utils.modbus_values.HoldingRegisterSize(5))
        self.modbus_builder.set_timeout(utils.modbus_values.Timeout(3.0))
        self.modbus_builder.set_retries(utils.modbus_values.Retries(3))
        self.modbus_builder.set_reconnect_delay(utils.modbus_values.ReconnectDelay(0.1))
        self.modbus_builder.set_reconnect_delay_max(utils.modbus_values.ReconnectDelayMax(300.0))

        # Mock the factory to return the mock modbus interface
        self.modbus_factory.create_modbus.return_value = self.mock_modbus_interface

        # Create a concrete subclass of MVHR for testing
        class TestMVHR(MVHR):
            async def read_data(self):
                pass

            def __init__(self, config_loader: ConfigLoader, state_manager: StateManager, modbus_factory: ModbusFactory, builder: ModbusBuilder):
                super().__init__(config_loader, state_manager, modbus_factory)
                self.mock_modbus_interface = modbus_factory.create_modbus(
                    mode=ModbusMode.TCP,
                    builder=builder,
                    ip_address=IPAddress("192.168.0.100"),
                    port=Port(502)
                )

            @property
            def modbus(self) -> ModbusInterface:
                return self.mock_modbus_interface

        self.mvhr = TestMVHR(self.config_loader, self.state_manager, self.modbus_factory, self.modbus_builder)

    async def test_connect_successful(self):
        """Test that the connection succeeds."""
        self.mvhr.modbus.connect.return_value = None  # Simulate successful connection
        await self.mvhr.start()

        MagicMock(self.mvhr.modbus.connect).assert_called_once()  # Should only call connect once
        self.state_manager.update_state.assert_called_with(
            operational_states={MVHR_RUNNING: True}
        )

    async def test_connect_failure(self):
        """Test that the connection fails and the correct state is updated."""
        self.mvhr.modbus.connect.side_effect = Exception("Connection failed")
        await self.mvhr.start()

        MagicMock(self.mvhr.modbus.connect).assert_called_once()  # Should only call connect once
        self.state_manager.update_state.assert_called_with(
            operational_states={MVHR_RUNNING: False},
            triggered_rules={MVHR_START_FAILURE: "Connection failed"}
        )

if __name__ == '__main__':
    unittest.main()
