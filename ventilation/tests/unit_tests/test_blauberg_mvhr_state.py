import unittest
from unittest.mock import MagicMock, PropertyMock
from blauberg.blauberg_mvhr_state import BlaubergMVHRState
from modbus.modbus import ModbusData
from utils.status import Status

class TestBlaubergMVHRState(unittest.TestCase):

    def setUp(self):
        # Mock the input_register values for valid temperatures
        self.mock_modbus_data = MagicMock(spec=ModbusData)

        # Create mock input_register values with a 'value' attribute
        mock_input_register = MagicMock()
        type(mock_input_register).value = PropertyMock(return_value=[
            0,     # IR_CUR_SEL_TEMP (not used in this test)
            250,   # IR_CURTEMP_SUAIR_IN -> 25.0°C
            300    # IR_CURTEMP_SUAIR_OUT -> 30.0°C
        ])

        # Set the input_register response to the mock
        self.mock_modbus_data.input_register = mock_input_register

    def test_temp_supply_in(self):
        """Test that the temp_supply_in is correctly initialized and returns the expected value."""
        # Initialize the state with mocked ModbusData
        mvhr_state = BlaubergMVHRState(data=self.mock_modbus_data)

        # Assert the temp_supply_in property returns the correct temperature
        self.assertEqual(mvhr_state.temp_supply_in.value, 25.0)  # 250 converted to 25.0°C

    def test_temp_supply_out(self):
        """Test that the temp_supply_out is correctly initialized and returns the expected value."""
        # Initialize the state with mocked ModbusData
        mvhr_state = BlaubergMVHRState(data=self.mock_modbus_data)

        # Assert the temp_supply_out property returns the correct temperature
        self.assertEqual(mvhr_state.temp_supply_out.value, 30.0)  # 300 converted to 30.0°C

    def test_no_sensor_detected(self):
        """Test that no sensor detection is handled correctly (-32768)."""
        # Update the mock to simulate no sensor detected
        type(self.mock_modbus_data.input_register).value = PropertyMock(return_value=[
            0,          # IR_CUR_SEL_TEMP (not used)
            -32768,     # IR_CURTEMP_SUAIR_IN -> No sensor detected
            300         # IR_CURTEMP_SUAIR_OUT -> 30.0°C
        ])

        # Initialize the state with mocked ModbusData
        mvhr_state = BlaubergMVHRState(data=self.mock_modbus_data)

        # Check that the response has a status of EXCEPTION and proper details for no sensor detection
        self.assertEqual(mvhr_state.temp_supply_in.status, Status.EXCEPTION)
        self.assertEqual(mvhr_state.temp_supply_in.details, "No sensor detected")
        self.assertIsNone(mvhr_state.temp_supply_in.value)

    def test_sensor_short_circuit(self):
        """Test that a sensor short circuit is handled correctly (32767)."""
        # Update the mock to simulate a short circuit
        type(self.mock_modbus_data.input_register).value = PropertyMock(return_value=[
            0,          # IR_CUR_SEL_TEMP (not used)
            250,        # IR_CURTEMP_SUAIR_IN -> 25.0°C
            32767       # IR_CURTEMP_SUAIR_OUT -> Short circuit
        ])

        # Initialize the state with mocked ModbusData
        mvhr_state = BlaubergMVHRState(data=self.mock_modbus_data)

        # Check that the response has a status of EXCEPTION and proper details for a short circuit
        self.assertEqual(mvhr_state.temp_supply_out.status, Status.EXCEPTION)
        self.assertEqual(mvhr_state.temp_supply_out.details, "Sensor short circuit")
        self.assertIsNone(mvhr_state.temp_supply_out.value)

if __name__ == '__main__':
    unittest.main()
