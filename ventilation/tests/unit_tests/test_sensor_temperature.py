import unittest
from unittest.mock import patch, MagicMock
from sensor.sensor_temperature import SensorTemperature
from utils.response import Response
from utils.status import Status
from utils.strategies import ExceptionCascadeStrategy
from utils.temperaturecelsius import LowTemperatureRange, HighTemperatureRange


class TestSensorTemperature(unittest.TestCase):

    def setUp(self):
        # Create mock responses and temperature ranges
        self.adc_response = Response(status=Status.OK, details="", value=1500)
        self.temp_low_range = LowTemperatureRange(value=0)
        self.temp_high_range = HighTemperatureRange(value=50)

    @patch('sensor.sensor_temperature.ExceptionCascadeStrategy')
    @patch('sensor.sensor_temperature.SensorDetectionStrategy')
    @patch('sensor.sensor_temperature.ADCToCurrentConversionStrategy')
    @patch('sensor.sensor_temperature.CurrentToTemperatureConversionStrategy')
    def test_specific_strategies_are_called(self, mock_current_to_temperature,
                                            mock_adc_to_current,
                                            mock_sensor_detection,
                                            mock_adc_exception_cascade):
        """Test that specific strategies are called during temperature processing."""
        # Mock the validate method to return an appropriate response object
        mock_adc_exception_cascade_instance = MagicMock()
        mock_adc_exception_cascade_instance.validate.return_value = Response(status=Status.OK, details="", value=250.0)
        mock_adc_exception_cascade.return_value = mock_adc_exception_cascade_instance

        mock_sensor_detection_instance = MagicMock()
        mock_sensor_detection_instance.validate.return_value = Response(status=Status.OK, details="", value=350.0)
        mock_sensor_detection.return_value = mock_sensor_detection_instance

        mock_adc_to_current_instance = MagicMock()
        mock_adc_to_current_instance.validate.return_value = Response(status=Status.OK, details="", value=450.0)
        mock_adc_to_current.return_value = mock_adc_to_current_instance

        mock_current_to_temperature_instance = MagicMock()
        mock_current_to_temperature_instance.validate.return_value = Response(status=Status.OK, details="", value=25.0)
        mock_current_to_temperature.return_value = mock_current_to_temperature_instance

        # Execute validation
        SensorTemperature(self.adc_response, self.temp_low_range, self.temp_high_range)

        # Ensure each strategy's validate method was called
        mock_adc_exception_cascade_instance.validate.assert_called_once_with(1500)
        mock_sensor_detection_instance.validate.assert_called_once_with(250)
        mock_adc_to_current_instance.validate.assert_called_once_with(350)
        mock_current_to_temperature_instance.validate.assert_called_once_with(450)

    def test_exception_cascade_strategy(self):
        """Test that ExceptionCascadeStrategy correctly handles cascading exceptions."""
        # Create a mock response with an EXCEPTION status
        error_response = Response(status=Status.EXCEPTION, details="Sensor error", value=None)
        strategy = ExceptionCascadeStrategy(response=error_response)

        # Validate and ensure the response is cascaded correctly
        response = strategy.validate(1500)
        self.assertEqual(response.status, Status.EXCEPTION)
        self.assertEqual(response.details, "Sensor error")
        self.assertIsNone(response.value)

if __name__ == '__main__':
    unittest.main()
