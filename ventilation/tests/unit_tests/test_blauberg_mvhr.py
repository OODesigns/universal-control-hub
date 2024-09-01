import unittest
from unittest.mock import MagicMock, AsyncMock
from blauberg.blauberg_mvhr import BlaubergMVHR
from blauberg.blauberg_mvhr_repository import BlaubergMVHRRepository
from blauberg.blauberg_registers import CoilRegister, DiscreteInputs, InputRegisters, HoldingRegister
from config.config_loader import ConfigLoader
from modbus.modbus import ModbusInterface, ModbusMode, ModbusData
from modbus.modbus_factory import ModbusFactory
from utils.tcp_values import IPAddress, Port
from utils.modbus_values import CoilSize, DiscreteInputSize, InputRegisterSize, HoldingRegisterSize
from utils.connection_reponse import ConnectionResponse, ConnectionStatus
from utils.value import ValidatedResponse, ValueStatus

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
        self.mock_modbus_interface = AsyncMock(spec=ModbusInterface)
        self.modbus_factory = MagicMock(spec=ModbusFactory)

        # Mock the factory to return the mock modbus interface
        self.modbus_factory.create_modbus.return_value = self.mock_modbus_interface

        # Initialize the BlaubergMVHR instance
        self.blauberg_mvhr = BlaubergMVHR(self.config_loader, self.modbus_factory)

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
        mock_response = ConnectionResponse(status=ConnectionStatus.OK, details="Connected successfully")
        self.mock_modbus_interface.connect.return_value = mock_response

        response = await self.blauberg_mvhr.start()

        # Ensure the connect method was called
        self.mock_modbus_interface.connect.assert_called_once()

        # Verify the response
        self.assertIsInstance(response, ConnectionResponse)
        self.assertEqual(response.status, ConnectionStatus.OK)
        self.assertEqual(response.details, "Connected successfully")

    async def test_modbus_startup_failure(self):
        """Test the failure handling during the startup sequence."""
        # Simulate a connection failure with an appropriate ConnectionResponse
        mock_response = ConnectionResponse(status=ConnectionStatus.FAILED, details="Connection failed")
        self.mock_modbus_interface.connect.return_value = mock_response

        response = await self.blauberg_mvhr.start()

        # Ensure the connect method was called
        self.mock_modbus_interface.connect.assert_called_once()

        # Verify the response
        self.assertIsInstance(response, ConnectionResponse)
        self.assertEqual(response.status, ConnectionStatus.FAILED)
        self.assertEqual(response.details, "Connection failed")

    async def test_modbus_stop(self):
        """Test the stop method of BlaubergMVHR."""
        # Simulate a successful disconnect
        mock_response = ConnectionResponse(status=ConnectionStatus.OK, details="Disconnected successfully")
        self.mock_modbus_interface.disconnect.return_value = mock_response

        # Call the stop method
        response = self.blauberg_mvhr.stop()

        # Ensure the disconnect method was called
        self.mock_modbus_interface.disconnect.assert_called_once()

        # Verify that the response is as expected
        self.assertIsInstance(response, ConnectionResponse)
        self.assertEqual(response.status, ConnectionStatus.OK)
        self.assertEqual(response.details, "Disconnected successfully")

    async def test_read_data(self):
        """Test that the read_data method returns a BlaubergMVHRRepository instance with correct data."""
        # Simulate Modbus read data
        mock_modbus_data = MagicMock()
        self.mock_modbus_interface.read.return_value = mock_modbus_data

        repository = await self.blauberg_mvhr.read_data()

        # Ensure the read method was called
        self.mock_modbus_interface.read.assert_called_once()

        # Verify that the repository is correctly returned
        self.assertIsInstance(repository, BlaubergMVHRRepository)
        self.assertEqual(repository.data, mock_modbus_data)

    async def test_read_data_with_temp_supply_in_out(self):
        """Test the read_data method with focus on temp_supply_in and temp_supply_out properties."""

        # Create a validated response that mimics successful Modbus data retrieval
        validated_response = ValidatedResponse(status=ValueStatus.OK, value=[
            0,    # IR_CUR_SEL_TEMP, not used in this test
            250,  # IR_CURTEMP_SUAIR_IN -> 25.0°C
            300   # IR_CURTEMP_SUAIR_OUT -> 30.0°C
        ], details="")

        # Create a mock ModbusData instance and set the validated response to input_register
        mock_modbus_data = MagicMock(spec=ModbusData)
        mock_modbus_data.input_register = validated_response.value

        # Simulate the Modbus interface returning this mock data
        self.mock_modbus_interface.read.return_value = mock_modbus_data

        # Call the read_data method, which will process the mock Modbus data
        repository = await self.blauberg_mvhr.read_data()

        # Assert the temperatures are correctly interpreted
        self.assertEqual(repository.temp_supply_in.value, 25.0)
        self.assertEqual(repository.temp_supply_out.value, 30.0)

    async def test_read_data_with_sensor_faults(self):
        """Test the read_data method with sensor fault values (-32768 and 32767)."""

        # Create a validated response that mimics Modbus data with faults
        validated_response = ValidatedResponse(status=ValueStatus.EXCEPTION, value=[
            0,       # IR_CUR_SEL_TEMP, not used in this test
            -32768,  # IR_CURTEMP_SUAIR_IN -> No sensor detected
            32767    # IR_CURTEMP_SUAIR_OUT -> Short circuit
        ], details="")

        # Create a mock ModbusData instance and set the validated response to input_register
        mock_modbus_data = MagicMock(spec=ModbusData)
        mock_modbus_data.input_register = validated_response.value

        # Simulate the Modbus interface returning this mock data
        self.mock_modbus_interface.read.return_value = mock_modbus_data

        # Call the read_data method, which will process the mock Modbus data
        repository = await self.blauberg_mvhr.read_data()

        # Test that accessing the faulty temperature values raises a ValueError
        with self.assertRaises(ValueError) as context_in:
            _ = repository.temp_supply_in.value
        self.assertEqual(str(context_in.exception), "Cannot access value: No sensor detected")

        with self.assertRaises(ValueError) as context_out:
            _ = repository.temp_supply_out.value
        self.assertEqual(str(context_out.exception), "Cannot access value: Sensor short circuit")

if __name__ == '__main__':
    unittest.main()
