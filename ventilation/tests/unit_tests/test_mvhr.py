import unittest
from unittest.mock import patch, MagicMock
from config.config_loader import ConfigLoader
from devices.modbus import ModbusFactory, ModbusInterface
from devices.mvhr import MVHR, MVHR_CONNECTED, MVHR_CONNECTION_FAILURE, MAX_RETRIES_REACHED
from state.state_manager import StateManager


class TestMVHRRetriesAsync(unittest.IsolatedAsyncioTestCase):

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
        self.mock_modbus_interface = MagicMock(spec=ModbusInterface)
        self.modbus_factory = MagicMock(spec=ModbusFactory)

        # Create a concrete subclass of MVHR for testing
        class TestMVHR(MVHR):
            def __init__(self, config_loader: ConfigLoader, state_manager: StateManager, modbus_factory: ModbusFactory):
                super().__init__(config_loader, state_manager, modbus_factory)
                self.mock_modbus_interface = MagicMock(spec=ModbusInterface)

            @property
            def get_modbus(self) -> ModbusInterface:
                return self.mock_modbus_interface

        self.mvhr = TestMVHR(self.config_loader, self.state_manager, self.modbus_factory)

    @patch('asyncio.sleep', return_value=None)  # Patch asyncio sleep to skip delays during testing
    async def test_connect_successful_first_attempt(self, mock_sleep):
        """Test that the connection succeeds on the first attempt without retries."""
        self.mock_modbus_interface.connect.return_value = None  # Simulate successful connection

        success = await self.mvhr.connect_with_retries()

        self.assertTrue(success)
        self.mock_modbus_interface.connect.assert_called_once()  # Should only call connect once
        self.state_manager.update_state.assert_called_with(
            operational_states={MVHR_CONNECTED: True}
        )
        mock_sleep.assert_not_called()  # No sleep calls should be made

    @patch('asyncio.sleep', return_value=None)
    async def test_connect_successful_after_retries(self, mock_sleep):
        """Test that the connection succeeds after a few retries."""
        # Simulate failure on first two attempts, success on the third
        self.mock_modbus_interface.connect.side_effect = [Exception("Connection failed"),
                                                          Exception("Connection failed"), None]

        success = await self.mvhr.connect_with_retries()

        self.assertTrue(success)
        self.assertEqual(self.mock_modbus_interface.connect.call_count, 3)  # Should try connecting 3 times
        self.state_manager.update_state.assert_any_call(
            operational_states={MVHR_CONNECTED: False},
            triggered_rules={MVHR_CONNECTION_FAILURE: 'Connection failed'}
        )
        self.state_manager.update_state.assert_called_with(
            operational_states={MVHR_CONNECTED: True}
        )
        self.assertEqual(mock_sleep.call_count, 2)  # Sleep should be called twice

    @patch('asyncio.sleep', return_value=None)
    async def test_connect_fails_after_max_retries(self, mock_sleep):
        """Test that the connection fails after the maximum number of retries."""
        self.mock_modbus_interface.connect.side_effect = Exception("Connection failed")  # Always fail

        success = await self.mvhr.connect_with_retries()

        self.assertFalse(success)
        self.assertEqual(self.mock_modbus_interface.connect.call_count,
                         self.mvhr.max_retries)  # Should try max_retries times
        self.state_manager.update_state.assert_any_call(
            operational_states={MVHR_CONNECTED: False},
            triggered_rules={MVHR_CONNECTION_FAILURE: 'Connection failed'}
        )
        self.state_manager.update_state.assert_called_with(
            operational_states={MVHR_CONNECTED: False},
            triggered_rules={MVHR_CONNECTION_FAILURE: MAX_RETRIES_REACHED}
        )
        self.assertEqual(mock_sleep.call_count,
                         self.mvhr.max_retries - 1)  # Sleep called for each retry except the last one

    @patch('asyncio.sleep', return_value=None)
    async def test_exponential_backoff(self, mock_sleep):
        """Test that the delays between retries follow an exponential backoff pattern."""
        # Simulate failure on all but the last attempt
        self.mock_modbus_interface.connect.side_effect = [Exception("Connection failed")] * (
                    self.mvhr.max_retries - 1) + [None]

        await self.mvhr.connect_with_retries()

        expected_delays = [self.mvhr.base_delay * (2 ** i) for i in range(self.mvhr.max_retries - 1)]
        for i, expected_delay in enumerate(expected_delays):
            # Check that sleep was called with the correct delay
            self.assertEqual(mock_sleep.call_args_list[i][0][0], min(expected_delay, self.mvhr.max_delay))

    @patch('asyncio.sleep', return_value=None)
    async def test_start_method(self):
        """Test the start method for non-blocking execution and successful connection."""
        # Simulate failure on first attempt, success on the second
        self.mock_modbus_interface.connect.side_effect = [Exception("Connection failed"), None]

        await self.mvhr.start()

        self.assertEqual(self.mock_modbus_interface.connect.call_count, 2)
        self.state_manager.update_state.assert_any_call(
            operational_states={MVHR_CONNECTED: False},
            triggered_rules={MVHR_CONNECTION_FAILURE: 'Connection failed'}
        )
        self.state_manager.update_state.assert_called_with(
            operational_states={MVHR_CONNECTED: True}
        )


if __name__ == '__main__':
    unittest.main()
