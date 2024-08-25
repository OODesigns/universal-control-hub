import unittest
from unittest import TestCase
from utils.temperaturecelsius import TemperatureCelsius, StrictTemperatureCelsius
from utils.value import ValueStatus

class TestTemperature(TestCase):

    def test_valid_temperature(self):
        """Test creation of Temperature with valid values"""
        t = TemperatureCelsius(25.5)
        self.assertEqual(t.value, 25.5)
        self.assertEqual(t.status, ValueStatus.OK)
        self.assertEqual(t.details, "")

    def test_temperature_below_range(self):
        """Test that temperature below -20 returns a validation result with EXCEPTION status"""
        t = TemperatureCelsius(-25)
        self.assertEqual(t.status, ValueStatus.EXCEPTION)
        self.assertEqual(t.details, "Temperature must be between -20 and 50°C.")

    def test_temperature_above_range(self):
        """Test that temperature above 50 returns a validation result with EXCEPTION status"""
        t = TemperatureCelsius(55)
        self.assertEqual(t.status, ValueStatus.EXCEPTION)
        self.assertEqual(t.details, "Temperature must be between -20 and 50°C.")

    def test_temperature_at_lower_boundary(self):
        """Test that temperature at the lower boundary (-20°C) is valid"""
        t = TemperatureCelsius(-20)
        self.assertEqual(t.value, -20)
        self.assertEqual(t.status, ValueStatus.OK)
        self.assertEqual(t.details, "")

    def test_temperature_at_upper_boundary(self):
        """Test that temperature at the upper boundary (50°C) is valid"""
        t = TemperatureCelsius(50)
        self.assertEqual(t.value, 50)
        self.assertEqual(t.status, ValueStatus.OK)
        self.assertEqual(t.details, "")

class TestStrictTemperature(TestCase):

    def test_strict_temperature_success(self):
        """Test that a valid temperature does not raise an error"""
        strict_t = StrictTemperatureCelsius(25.5)
        self.assertEqual(strict_t.value, 25.5)
        self.assertEqual(strict_t.status, ValueStatus.OK)
        self.assertEqual(strict_t.details, "")

    def test_strict_temperature_below_range(self):
        """Test that temperature below -20 raises a ValueError immediately"""
        with self.assertRaises(ValueError) as context:
            StrictTemperatureCelsius(-25)
        self.assertEqual("Validation failed for value '-25': Temperature must be between -20 and 50°C.",
                         str(context.exception))

    def test_strict_temperature_above_range(self):
        """Test that temperature above 50 raises a ValueError immediately"""
        with self.assertRaises(ValueError) as context:
            StrictTemperatureCelsius(55)
        self.assertEqual("Validation failed for value '55': Temperature must be between -20 and 50°C.",
                         str(context.exception))

    def test_strict_temperature_at_lower_boundary(self):
        """Test that temperature at the lower boundary (-20°C) is valid"""
        strict_t = StrictTemperatureCelsius(-20)
        self.assertEqual(strict_t.value, -20)
        self.assertEqual(strict_t.status, ValueStatus.OK)
        self.assertEqual(strict_t.details, "")

    def test_strict_temperature_at_upper_boundary(self):
        """Test that temperature at the upper boundary (50°C) is valid"""
        strict_t = StrictTemperatureCelsius(50)
        self.assertEqual(strict_t.value, 50)
        self.assertEqual(strict_t.status, ValueStatus.OK)
        self.assertEqual(strict_t.details, "")

if __name__ == '__main__':
    unittest.main()
