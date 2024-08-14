import unittest
from unittest.mock import Mock

from temperature import Temperature
from ventilation_config import VentilationConfiguration
from ventilation_mode import VentilationMode

class TestVentilationConfiguration(unittest.TestCase):

    def setUp(self):
        """Set up a mock Store object before each test."""
        self.mock_store = Mock()
        self.config = VentilationConfiguration(self.mock_store)

    def test_set_ventilation_mode(self):
        """Test that setting the ventilation mode stores it correctly."""
        self.config.ventilation_mode = VentilationMode.COOLING

        # Verify that the store's set method was called with the correct arguments
        self.mock_store.set.assert_called_once_with('ventilation_mode', 'COOLING')

    def test_get_ventilation_mode(self):
        """Test that getting the ventilation mode retrieves it correctly."""
        # Mock the return value of the store's get method
        self.mock_store.get.return_value = 'EXCHANGE'

        mode = self.config.ventilation_mode

        # Verify that the mode is retrieved correctly
        self.assertEqual(mode, VentilationMode.EXCHANGE)

        # Verify that the store's get method was called with the correct key
        self.mock_store.get.assert_called_once_with('ventilation_mode')

    def test_set_setpoint_temperature(self):
        """Test that setting the setpoint temperature stores it correctly."""
        temperature = Temperature(22.5)
        self.config.setpoint_temperature = temperature

        # Verify that the store's set method was called with the correct arguments
        self.mock_store.set.assert_called_once_with('setpoint_temperature', 22.5)

    def test_get_setpoint_temperature(self):
        """Test that getting the setpoint temperature retrieves it correctly."""
        # Mock the return value of the store's get method
        self.mock_store.get.return_value = 22

        temperature = self.config.setpoint_temperature

        # Verify that the temperature is retrieved correctly
        self.assertEqual(temperature.value, 22)

        # Verify that the store's get method was called with the correct key
        self.mock_store.get.assert_called_once_with('setpoint_temperature')

if __name__ == '__main__':
    unittest.main()
