import unittest
from unittest.mock import MagicMock, AsyncMock
from devices.blauberg_mvhr import BlaubergMVHR
from config.config_loader import ConfigLoader
from modbus.modbus import ModbusInterface, ModbusMode
from modbus.modbus_factory import ModbusFactory
from state.state_manager import StateManager
from utils.tcp_values import IPAddress, Port
from utils.modbus_values import CoilSize, DiscreteInputSize, InputRegisterSize, HoldingRegisterSize
from devices.blauberg_registers import CoilRegister, DiscreteInputs, InputRegisters, HoldingRegister

class TestBlaubergMVHR(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        # Mock the ConfigLoader to avoid needing a real config file
        self.config_loader = MagicMock(spec=ConfigLoader)
        self.config_loader.get_value.side_effect = lambda key, default=None: {
            'mvhr-timeout': 10,
            'mvhr-port': 502,
            'mvhr-ip-address': '192.168.0.100',
            'mvhr-retries': 3,
            'mvhr-reconnect-delay': 0.1,
            'mvhr-reconnect-delay-max': 300.0,
        }.get(key, default)

        # Set up the state manager and mock modbus
        self.state_manager = MagicMock(spec=StateManager)
        self.mock_modbus_interface = AsyncMock(spec=ModbusInterface)
        self.modbus_factory = MagicMock(spec=ModbusFactory)

        # Mock the factory to return the mock modbus interface
        self.modbus_factory.create_modbus.return_value = self.mock_modbus_interface

        # Initialize the BlaubergMVHR instance
        self.blauberg_mvhr = BlaubergMVHR(self.config_loader, self.state_manager, self.modbus_factory)

    async def test_modbus_initialization(self):
        """Test that the Modbus interface is initialized with the correct parameters."""
        self.modbus_factory.create_modbus.assert_called_once()
        call_args = self.modbus_factory.create_modbus.call_args[1]

        self.assertEqual(call_args['mode'], ModbusMode.TCP)
        self.assertEqual(call_args['ip_address'], IPAddress('192.168.0.100'))
        self.assertEqual(call_args['port'], Port(502))

        # Check builder configuration through the arguments passed during creation
        builder = call_args['builder']
        self.assertIsInstance(builder.coil_size, CoilSize)
        self.assertIsInstance(builder.discrete_input_size, DiscreteInputSize)
        self.assertIsInstance(builder.input_register_size, InputRegisterSize)
        self.assertIsInstance(builder.holding_register_size, HoldingRegisterSize)

        self.assertEqual(builder.coil_size.value, CoilRegister.CL_SIZE.value)
        self.assertEqual(builder.discrete_input_size.value, DiscreteInputs.DI_SIZE.value)
        self.assertEqual(builder.input_register_size.value, InputRegisters.IR_SIZE.value)
        self.assertEqual(builder.holding_register_size.value, HoldingRegister.HR_SIZE.value)
        self.assertEqual(builder.timeout.value, 10)
        self.assertEqual(builder.retries.value, 3)
        self.assertEqual(builder.reconnect_delay.value, 0.1)
        self.assertEqual(builder.reconnect_delay_max.value, 300.0)

    async def test_modbus_startup(self):
        """Test the startup sequence of the BlaubergMVHR."""
        # Simulate a successful connection
        self.mock_modbus_interface.connect.return_value = None
        await self.blauberg_mvhr.start()

        self.mock_modbus_interface.connect.assert_called_once()
        self.state_manager.update_state.assert_called_once_with(
            operational_states={'mvhr_connected': True}
        )

    async def test_modbus_startup_failure(self):
        """Test the failure handling during the startup sequence."""
        # Simulate a connection failure
        self.mock_modbus_interface.connect.side_effect = Exception("Connection failed")
        await self.blauberg_mvhr.start()

        self.mock_modbus_interface.connect.assert_called_once()
        self.state_manager.update_state.assert_called_once_with(
            operational_states={'mvhr_connected': False},
            triggered_rules={'mvhr_connection_failure': 'Connection failed'}
        )


if __name__ == '__main__':
    unittest.main()
