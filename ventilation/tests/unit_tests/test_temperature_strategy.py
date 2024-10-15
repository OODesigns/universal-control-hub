import unittest
from sensor.temperture_strategy import ADCToCurrentConversionStrategy, CurrentToTemperatureConversionStrategy, \
    RestrictedRangeValidationStrategy, MAX_CURRENT_MA, MIN_CURRENT_MA, SensorDetection
from utils.response import Status


class TestTemperatureStrategies(unittest.TestCase):

    def test_sensor_detection_no_sensor(self):
        """Test that SensorDetection detects no sensor when ADC value is below the open circuit threshold."""
        strategy = SensorDetection()
        response = strategy.validate(800)  # Below the open circuit threshold (819)
        self.assertEqual(response.status, Status.EXCEPTION)
        self.assertEqual(response.details, "No sensor detected")

    def test_sensor_detection_short_circuit(self):
        """Test that SensorDetection detects a sensor short circuit when ADC value is above the short circuit threshold."""
        strategy = SensorDetection()
        response = strategy.validate(3940)  # Above the short circuit threshold (3932)
        self.assertEqual(response.status, Status.EXCEPTION)
        self.assertEqual(response.details, "Sensor short circuit detected")

    def test_sensor_detection_valid(self):
        """Test that SensorDetection passes when ADC value is within the valid range."""
        strategy = SensorDetection()
        response = strategy.validate(2000)  # Within the valid range (819 - 3932)
        self.assertEqual(response.status, Status.OK)
        self.assertEqual(response.details, "Sensor detection successful")

    def test_adc_to_current_conversion(self):
        """Test that ADCToCurrentConversionStrategy converts an ADC value to current (mA)."""
        strategy = ADCToCurrentConversionStrategy()
        adc_value = 2048  # Mid-point ADC value

        response = strategy.validate(adc_value)
        expected_current = (((2048 / (4096-1)) * 5) / 240) * 1000
        self.assertEqual(response.status, Status.OK)
        self.assertAlmostEqual(response.value, expected_current, places=2)

    def test_current_to_temperature_conversion(self):
        """Test that CurrentToTemperatureConversionStrategy converts current to temperature."""
        strategy = CurrentToTemperatureConversionStrategy(min_temp=0, max_temp=50)
        response = strategy.validate(12.0)  # Mid-range current
        expected_temperature = ((12.0 - MIN_CURRENT_MA) / (MAX_CURRENT_MA - MIN_CURRENT_MA)) * 50
        self.assertEqual(response.status, Status.OK)
        self.assertAlmostEqual(response.value, expected_temperature, places=2)

    def test_current_to_temperature_out_of_range(self):
        """Test that CurrentToTemperatureConversionStrategy fails if the current is out of range."""
        strategy = CurrentToTemperatureConversionStrategy(min_temp=0, max_temp=50)
        response = strategy.validate(22.0)  # Out of range current (above 20 mA)
        self.assertEqual(response.status, Status.EXCEPTION)
        self.assertEqual(response.details, "Current 22.0 is out of range")

    def test_restricted_range_validation_valid(self):
        """Test that RestrictedRangeValidationStrategy passes for valid temperature."""
        strategy = RestrictedRangeValidationStrategy(min_temp=0, max_temp=50)
        response = strategy.validate(25.0)  # Valid temperature
        self.assertEqual(response.status, Status.OK)
        self.assertEqual(response.details, "Temperature validation successful")

    def test_restricted_range_validation_out_of_range(self):
        """Test that RestrictedRangeValidationStrategy fails for out of range temperature."""
        strategy = RestrictedRangeValidationStrategy(min_temp=0, max_temp=50)
        response = strategy.validate(55.0)  # Out of range temperature
        self.assertEqual(response.status, Status.EXCEPTION)
        self.assertEqual(response.details, "Temperature 55.0 out of range")


if __name__ == '__main__':
    unittest.main()