import unittest
from utils.temperaturecelsius import TemperatureCelsius, StrictTemperatureCelsius, LowTemperatureRange, \
    HighTemperatureRange
from utils.status import Status

class TestTemperature(unittest.TestCase):

    # Non-strict validation tests for TemperatureCelsius
    def test_valid_temperature(self):
        """Test creation of Temperature with valid values"""
        t = TemperatureCelsius(25.5)
        self.assertEqual(t.value, 25.5)
        self.assertEqual(t.status, Status.OK)
        self.assertEqual(t.details, "Valid temperature in Celsius")  # Updated expected message

    def test_temperature_below_range(self):
        """Test that temperature below -20 returns a validation result with EXCEPTION status"""
        t = TemperatureCelsius(-25)
        self.assertEqual(t.status, Status.EXCEPTION)
        self.assertEqual(t.details, "Value must be greater than or equal to -20.0, got -25")
        self.assertIsNone(t.value)

    def test_temperature_above_range(self):
        """Test that temperature above 50 returns a validation result with EXCEPTION status"""
        t = TemperatureCelsius(55)
        self.assertEqual(t.status, Status.EXCEPTION)
        self.assertEqual(t.details, "Value must be less than or equal to 50.0, got 55")
        self.assertIsNone(t.value)

    def test_temperature_at_lower_boundary(self):
        """Test that temperature at the lower boundary (-20°C) is valid"""
        t = TemperatureCelsius(-20)
        self.assertEqual(t.value, -20)
        self.assertEqual(t.status, Status.OK)
        self.assertEqual(t.details, "Valid temperature in Celsius")  # Updated expected message

    def test_temperature_at_upper_boundary(self):
        """Test that temperature at the upper boundary (50°C) is valid"""
        t = TemperatureCelsius(50)
        self.assertEqual(t.value, 50)
        self.assertEqual(t.status, Status.OK)
        self.assertEqual(t.details, "Valid temperature in Celsius")  # Updated expected message


class TestStrictTemperature(unittest.TestCase):

    # Strict validation tests for StrictTemperatureCelsius
    def test_strict_temperature_success(self):
        """Test that a valid temperature does not raise an error"""
        strict_t = StrictTemperatureCelsius(25.5)
        self.assertEqual(strict_t.value, 25.5)
        self.assertEqual(strict_t.status, Status.OK)
        self.assertEqual(strict_t.details, "Valid temperature in Celsius")  # Updated expected message

    def test_strict_temperature_below_range(self):
        """Test that temperature below -20 raises a ValueError immediately"""
        with self.assertRaises(ValueError) as context:
            StrictTemperatureCelsius(-25)
        self.assertEqual(
            str(context.exception),
            "Validation failed for value '-25': Value must be greater than or equal to -20.0, got -25"
        )

    def test_strict_temperature_above_range(self):
        """Test that temperature above 50 raises a ValueError immediately"""
        with self.assertRaises(ValueError) as context:
            StrictTemperatureCelsius(55)
        self.assertEqual(
            str(context.exception),
            "Validation failed for value '55': Value must be less than or equal to 50.0, got 55"
        )

    def test_strict_temperature_at_lower_boundary(self):
        """Test that temperature at the lower boundary (-20°C) is valid"""
        strict_t = StrictTemperatureCelsius(-20)
        self.assertEqual(strict_t.value, -20)
        self.assertEqual(strict_t.status, Status.OK)
        self.assertEqual(strict_t.details, "Valid temperature in Celsius")  # Updated expected message

    def test_strict_temperature_at_upper_boundary(self):
        """Test that temperature at the upper boundary (50°C) is valid"""
        strict_t = StrictTemperatureCelsius(50)
        self.assertEqual(strict_t.value, 50)
        self.assertEqual(strict_t.status, Status.OK)
        self.assertEqual(strict_t.details, "Valid temperature in Celsius")  # Updated expected message

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
