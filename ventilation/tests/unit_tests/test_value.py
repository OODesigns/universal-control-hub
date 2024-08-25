import unittest

from utils.value import Value, ValidatedResult, ValueStatus, ValidatedValue, StrictValidatedValue


class TestValue(unittest.TestCase):

    def test_value_initialization(self):
        v = Value(10)
        self.assertEqual(v.value, 10)

    def test_value_equality(self):
        v1 = Value(10)
        v2 = Value(10)
        v3 = Value(20)
        self.assertTrue(v1 == v2)
        self.assertFalse(v1 == v3)

    def test_value_comparison(self):
        v1 = Value(10)
        v2 = Value(20)
        self.assertTrue(v1 < v2)
        self.assertTrue(v1 <= v2)
        self.assertFalse(v2 < v1)
        self.assertFalse(v2 <= v1)

    def test_value_invalid_comparison(self):
        v1 = Value(10)
        self.assertFalse(v1 == 10)

class TestValidatedResult(unittest.TestCase):

    def test_validated_result_initialization(self):
        result = ValidatedResult(status=ValueStatus.OK, details="All good", value=100)
        self.assertEqual(result.status, ValueStatus.OK)
        self.assertEqual(result.details, "All good")
        self.assertEqual(result.value, 100)

class MockValidatedValue(ValidatedValue):

    @classmethod
    def validate(cls, validated_value) -> ValidatedResult:
        if validated_value is None:
            return ValidatedResult(status=ValueStatus.EXCEPTION, details="Invalid value", value=None)
        return ValidatedResult(status=ValueStatus.OK, details="Valid value", value=validated_value)

class TestValidatedValue(unittest.TestCase):

    def test_validated_value_success(self):
        v = MockValidatedValue(100)
        self.assertEqual(v.value, 100)
        self.assertEqual(v.status, ValueStatus.OK)
        self.assertEqual(v.details, "Valid value")

    def test_validated_value_failure(self):
        v = MockValidatedValue(None)
        self.assertEqual(v.status, ValueStatus.EXCEPTION)
        self.assertEqual(v.details, "Invalid value")
        with self.assertRaises(ValueError):
            _ = v.value  # Should raise ValueError since validation failed

    def test_validated_value_comparison(self):
        v1 = MockValidatedValue(10)
        v2 = MockValidatedValue(20)
        v3 = MockValidatedValue(10)
        v4 = MockValidatedValue(None)  # Invalid value

        self.assertTrue(v1 < v2)
        self.assertTrue(v1 <= v2)
        self.assertTrue(v1 == v3)
        self.assertFalse(v1 < v3)
        self.assertFalse(v1 > v3)
        self.assertFalse(v4 == v1)  # Can't compare invalid with valid

class MockStrictValidatedValue(StrictValidatedValue):
    @classmethod
    def validate(cls, validated_value) -> ValidatedResult:
        if validated_value is None:
            return ValidatedResult(status=ValueStatus.EXCEPTION, details="Invalid value", value=None)
        return ValidatedResult(status=ValueStatus.OK, details="Valid value", value=validated_value)

class TestStrictValidatedValue(unittest.TestCase):

    def test_strict_validated_value_success(self):
        strict_v = MockStrictValidatedValue(100)
        self.assertEqual(strict_v.value, 100)
        self.assertEqual(strict_v.status, ValueStatus.OK)
        self.assertEqual(strict_v.details, "Valid value")

    def test_strict_validated_value_failure(self):
        with self.assertRaises(ValueError):
            MockStrictValidatedValue(None)  # Should raise ValueError immediately


