import unittest
from unittest.mock import Mock

from utils.temperaturecelsius import TemperatureCelsius
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
        self.mock_store.set_value.assert_called_once_with('ventilation_mode', VentilationMode.COOLING)

    def test_get_ventilation_mode(self):
        """Test that getting the ventilation mode retrieves it correctly."""
        # Mock the return value of the store's get method
        self.mock_store.get_value.return_value = VentilationMode.EXCHANGE

        mode = self.config.ventilation_mode

        # Verify that the mode is retrieved correctly
        self.assertEqual(mode, VentilationMode.EXCHANGE)

        # Verify that the store's get method was called with the correct key
        self.mock_store.get_value.assert_called_once_with('ventilation_mode')

    def test_set_set_point_temperature(self):
        """Test that setting the set-point temperature stores it correctly."""
        temperature = TemperatureCelsius(22.5)
        self.config.set_point_temperature = temperature

        # Verify that the store's set method was called with the correct arguments
        self.mock_store.set_value.assert_called_once_with('set_point_temperature', TemperatureCelsius(22.5))

    def test_get_set_point_temperature(self):
        """Test that getting the set-point temperature retrieves it correctly."""
        # Mock the return value of the store's get method
        self.mock_store.get_value.return_value = 22

        temperature = self.config.set_point_temperature

        # Verify that the temperature is retrieved correctly
        self.assertTrue(temperature == TemperatureCelsius(22))

        # Verify that the store's get method was called with the correct key
        self.mock_store.get_value.assert_called_once_with('set_point_temperature')


if __name__ == '__main__':
    unittest.main()
