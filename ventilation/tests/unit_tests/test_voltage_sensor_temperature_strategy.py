import unittest

from sensor.voltage_temperature_temperature_strategy import ADCToTemperatureConversionStrategy
from utils.response import Status
from utils.temperaturecelsius import LowTemperatureRange, HighTemperatureRange


class TestADCToTemperatureConversionStrategy(unittest.TestCase):

    def test_adc_to_temperature_conversion_min_value(self):
        """Test that ADCToTemperatureConversionStrategy converts the minimum ADC value to the correct temperature."""
        strategy = ADCToTemperatureConversionStrategy(LowTemperatureRange(0), HighTemperatureRange(50))
        adc_value = 0  # Minimum ADC value

        response = strategy.validate(adc_value)
        self.assertEqual(response.status, Status.OK)
        self.assertEqual(response.value, 0.0)

    def test_adc_to_temperature_conversion_max_value(self):
        """Test that ADCToTemperatureConversionStrategy converts the maximum ADC value to the correct temperature."""
        strategy = ADCToTemperatureConversionStrategy(LowTemperatureRange(0), HighTemperatureRange(50))
        adc_value = 4095  # Maximum ADC value

        response = strategy.validate(adc_value)
        self.assertEqual(response.status, Status.OK)
        self.assertEqual(response.value, 50.0)

    def test_adc_to_temperature_conversion_mid_value(self):
        """Test that ADCToTemperatureConversionStrategy converts a mid-range ADC value to the correct temperature."""
        strategy = ADCToTemperatureConversionStrategy(LowTemperatureRange(0), HighTemperatureRange(50))
        adc_value = 2048  # Mid-range ADC value

        response = strategy.validate(adc_value)
        self.assertEqual(response.status, Status.OK)
        self.assertAlmostEqual(response.value, 25.0, places=1)

    def test_adc_to_temperature_out_of_range_low(self):
        """Test that ADCToTemperatureConversionStrategy handles ADC values below the valid range."""
        strategy = ADCToTemperatureConversionStrategy(LowTemperatureRange(0), HighTemperatureRange(50))
        adc_value = -1  # Below minimum ADC value

        response = strategy.validate(adc_value)
        self.assertEqual(response.status, Status.EXCEPTION)
        self.assertEqual(response.details, "ADC value -1 is out of range")

    def test_adc_to_temperature_out_of_range_high(self):
        """Test that ADCToTemperatureConversionStrategy handles ADC values above the valid range."""
        strategy = ADCToTemperatureConversionStrategy(LowTemperatureRange(0), HighTemperatureRange(50))
        adc_value = 5000  # Above maximum ADC value

        response = strategy.validate(adc_value)
        self.assertEqual(response.status, Status.EXCEPTION)
        self.assertEqual(response.details, "ADC value 5000 is out of range")


if __name__ == '__main__':
    unittest.main()
