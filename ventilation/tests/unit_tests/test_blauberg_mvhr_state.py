import unittest
from unittest.mock import MagicMock
from blauberg.blauberg_mvhr_state import BlaubergMVHRState
from modbus.modbus import ModbusData
from utils.status import Status
from utils.response import Response

class TestBlaubergMVHRState(unittest.TestCase):

    def setUp(self):
        # Mock the input_register values for valid temperatures
        self.mock_modbus_data = MagicMock(spec=ModbusData)

        # Set the input_register response to the mock
        self.mock_modbus_data.input_register = Response(
            status=Status.OK,
            details="Valid input register data",
            value=[0, 250, 300]
        )

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
        self.mock_modbus_data.input_register = Response(
            status=Status.OK,
            details="Valid input register data",
            value=[0,-32768,300]
        )

        # Initialize the state with mocked ModbusData
        mvhr_state = BlaubergMVHRState(data=self.mock_modbus_data)

        # Check that the response has a status of EXCEPTION and proper details for no sensor detection
        self.assertEqual(mvhr_state.temp_supply_in.status, Status.EXCEPTION)
        self.assertEqual(mvhr_state.temp_supply_in.details, "No sensor detected")
        self.assertIsNone(mvhr_state.temp_supply_in.value)

    def test_sensor_short_circuit(self):
        """Test that a sensor short circuit is handled correctly (32767)."""
        self.mock_modbus_data.input_register = Response(
            status=Status.OK,
            details="Valid input register data",
            value=[0,250,32767]
        )

        # Initialize the state with mocked ModbusData
        mvhr_state = BlaubergMVHRState(data=self.mock_modbus_data)

        # Check that the response has a status of EXCEPTION and proper details for a short circuit
        self.assertEqual(mvhr_state.temp_supply_out.status, Status.EXCEPTION)
        self.assertEqual(mvhr_state.temp_supply_out.details, "Sensor short circuit")
        self.assertIsNone(mvhr_state.temp_supply_out.value)

    def test_invalid_input_register(self):
        """Test handling an invalid input register selection."""
        # Update the mock to simulate an out-of-bounds input register selection
        self.mock_modbus_data.input_register = Response(
            status=Status.OK,
            details="Valid input register data",
            value=[0,250]
        )

        # Initialize the state with mocked ModbusData
        mvhr_state = BlaubergMVHRState(data=self.mock_modbus_data)

        self.assertEqual(mvhr_state.temp_supply_out.status, Status.EXCEPTION)
        self.assertEqual(mvhr_state.temp_supply_out.details,"Register selection out of bounds of input register")

if __name__ == '__main__':
    unittest.main()