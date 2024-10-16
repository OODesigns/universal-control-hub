import unittest
from sensor.temperture_strategy import (ADCToCurrentConversionStrategy,
                                        CurrentToTemperatureConversionStrategy,
                                        SensorDetectionStrategy)
from utils.response import Status


class TestTemperatureStrategies(unittest.TestCase):

    def test_sensor_detection_no_sensor(self):
        """Test that SensorDetection detects no sensor when ADC value is below the open circuit threshold."""
        strategy = SensorDetectionStrategy()
        response = strategy.validate(780)  # Below the open circuit threshold (786)
        self.assertEqual(response.status, Status.EXCEPTION)
        self.assertEqual(response.details, "No sensor detected")

    def test_sensor_detection_short_circuit(self):
        """Test that SensorDetection detects a sensor short circuit when ADC value is above the short circuit threshold."""
        strategy = SensorDetectionStrategy()
        response = strategy.validate(3940)  # Above the short circuit threshold (3932)
        self.assertEqual(response.status, Status.EXCEPTION)
        self.assertEqual(response.details, "Sensor short circuit detected")

    def test_sensor_detection_valid(self):
        """Test that SensorDetection passes when ADC value is within the valid range."""
        strategy = SensorDetectionStrategy()
        response = strategy.validate(1500)  # Within the valid range (819 - 3932)
        self.assertEqual(response.status, Status.OK)
        self.assertEqual(response.details, "Sensor detection successful")

    def test_adc_to_current_conversion_min_value(self):
        """Test that ADCToCurrentConversionStrategy converts the minimum ADC value to the correct current (mA)."""
        strategy = ADCToCurrentConversionStrategy()
        adc_value = 786  # Minimum ADC value corresponding to 4mA

        response = strategy.validate(adc_value)
        expected_current = (((adc_value / 4095) * 5) / 240) * 1000
        self.assertEqual(response.status, Status.OK)
        self.assertAlmostEqual(response.value, expected_current, places=2)

    def test_adc_to_current_conversion_max_value(self):
        """Test that ADCToCurrentConversionStrategy converts the maximum ADC value to the correct current (mA)."""
        strategy = ADCToCurrentConversionStrategy()
        adc_value = 3932  # Maximum ADC value corresponding to 20mA

        response = strategy.validate(adc_value)
        expected_current = (((adc_value / 4095) * 5) / 240) * 1000
        self.assertEqual(response.status, Status.OK)
        self.assertAlmostEqual(response.value, expected_current, places=2)

    def test_current_to_temperature_conversion(self):
        """Test that CurrentToTemperatureConversionStrategy converts current to temperature."""
        strategy = CurrentToTemperatureConversionStrategy(min_temp=0, max_temp=50)
        response = strategy.validate(12.0)  # Mid-range current
        expected_temperature = ((12.0 - 4) / (20 - 4)) * 50
        self.assertEqual(response.status, Status.OK)
        self.assertAlmostEqual(response.value, expected_temperature, places=2)

    def test_current_to_temperature_out_of_range(self):
        """Test that CurrentToTemperatureConversionStrategy fails if the current is out of range."""
        strategy = CurrentToTemperatureConversionStrategy(min_temp=0, max_temp=50)
        response = strategy.validate(22.0)  # Out of range current (above 20 mA)
        self.assertEqual(response.status, Status.EXCEPTION)
        self.assertEqual(response.details, "Current 22.0 is out of range")


if __name__ == '__main__':
    unittest.main()