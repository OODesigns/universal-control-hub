import unittest

from sensor.sensor_temperature_range import LowTemperatureRange, HighTemperatureRange
from utils.status import Status

class TestTemperatureRange(unittest.TestCase):

    def test_low_temperature_range_valid(self):
        # Valid values within the range -20 to 0
        valid_values = [-20, -10, 0]
        for value in valid_values:
            temp = LowTemperatureRange(value)
            self.assertEqual(temp.status, Status.OK)
            self.assertEqual(temp.value, value)

    def test_low_temperature_range_invalid(self):
        # Invalid values outside the range -20 to 0
        invalid_values = [-21, 1, 50]
        for value in invalid_values:
            temp = LowTemperatureRange(value)
            self.assertEqual(temp.status, Status.EXCEPTION)
            self.assertIsNone(temp.value)

    def test_high_temperature_range_valid(self):
        # Valid values within the range 40 to 50
        valid_values = [40, 45, 50]
        for value in valid_values:
            temp = HighTemperatureRange(value)
            self.assertEqual(temp.status, Status.OK)
            self.assertEqual(temp.value, value)

    def test_high_temperature_range_invalid(self):
        # Invalid values outside the range 40 to 50
        invalid_values = [39, 51, 0]
        for value in invalid_values:
            temp = HighTemperatureRange(value)
            self.assertEqual(temp.status, Status.EXCEPTION)
            self.assertIsNone(temp.value)

if __name__ == '__main__':
    unittest.main()
