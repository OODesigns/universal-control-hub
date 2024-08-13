import unittest
from unittest import TestCase

from temperature import Temperature


class TestTemperature(TestCase):
    def test_valid_temperature(self):
        """Test creation of Temperature with valid values"""
        try:
            t = Temperature(25)
            self.assertEqual(t._value, 25)
        except Exception as e:
            self.fail(f"Temperature(25) raised {type(e).__name__} unexpectedly!")

    def test_temperature_below_range(self):
        """Test that temperature below 0 raises a ValueError"""
        with self.assertRaises(ValueError) as context:
            Temperature(-5)
        self.assertEqual(str(context.exception), "Temperature must be between 0 and 50°C.")

    def test_temperature_above_range(self):
        """Test that temperature above 50 raises a ValueError"""
        with self.assertRaises(ValueError) as context:
            Temperature(55)
        self.assertEqual(str(context.exception), "Temperature must be between 0 and 50°C.")

    def test_temperature_at_lower_boundary(self):
        """Test that temperature at the lower boundary (0°C) is valid"""
        try:
            t = Temperature(0)
            self.assertEqual(t._value, 0)
        except Exception as e:
            self.fail(f"Temperature(0) raised {type(e).__name__} unexpectedly!")

    def test_temperature_at_upper_boundary(self):
        """Test that temperature at the upper boundary (50°C) is valid"""
        try:
            t = Temperature(50)
            self.assertEqual(t._value, 50)
        except Exception as e:
            self.fail(f"Temperature(50) raised {type(e).__name__} unexpectedly!")


if __name__ == '__main__':
    unittest.main()
