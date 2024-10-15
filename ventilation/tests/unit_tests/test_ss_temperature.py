import unittest
from sensor.ss_temperture import SSTemperature
from utils.response import Response
from utils.status import Status


class TestSSTemperature(unittest.TestCase):
    def setUp(self):
        # Set up valid ADC value within the expected range
        self.valid_adc_value = Response[int](status=Status.OK, details='Valid ADC', value=2000)
        # Set up ADC values to trigger different validation paths
        self.open_circuit_adc_value = Response[int](status=Status.OK, details='Open Circuit ADC', value=800)
        self.short_circuit_adc_value = Response[int](status=Status.OK, details='Short Circuit ADC', value=4000)
        self.out_of_range_adc_value = Response[int](status=Status.OK, details='Out of Range ADC', value=4097)

    def test_valid_temperature_conversion(self):
        # Test conversion from a valid ADC value to temperature
        temperature_sensor = SSTemperature(self.valid_adc_value)

        self.assertEqual(Status.OK, temperature_sensor.status)
        self.assertGreaterEqual(temperature_sensor.value, 0)
        self.assertLessEqual(temperature_sensor.value, 50)

    def test_open_circuit_detection(self):
        # Test sensor detection with open circuit ADC value
        temperature_sensor = SSTemperature(self.open_circuit_adc_value)

        self.assertEqual(Status.EXCEPTION,temperature_sensor.status)
        self.assertEqual(temperature_sensor.details, 'No sensor detected')

    def test_short_circuit_detection(self):
        # Test sensor detection with short circuit ADC value
        temperature_sensor = SSTemperature(self.short_circuit_adc_value)

        self.assertEqual(Status.EXCEPTION,temperature_sensor.status, )
        self.assertEqual(temperature_sensor.details, 'Sensor short circuit detected')

    def test_adc_out_of_range(self):
        # Test conversion when ADC value is out of range
        temperature_sensor = SSTemperature(self.out_of_range_adc_value)

        self.assertEqual(Status.EXCEPTION, temperature_sensor.status, )
        self.assertEqual(temperature_sensor.details, 'Sensor short circuit detected')

if __name__ == '__main__':
    unittest.main()