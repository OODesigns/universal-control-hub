import unittest
from utils.value import Value, ValidatedResponse, ValueStatus, ValidatedValue, StrictValidatedValue, RangeValidatedValue

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
        self.assertFalse(v1 == 10)  # Comparing with a non-Value type should return False
        self.assertFalse(v1 < 10)   # Should return False because `10` is not of type `Value`
        self.assertFalse(v1 <= 10)  # Should return False because `10` is not of type `Value`

        v2 = Value(20)
        self.assertFalse(v1 == v2)  # Check that equality with different values returns False


class TestValidatedResponse(unittest.TestCase):

    def test_validated_response_initialization(self):
        result = ValidatedResponse(status=ValueStatus.OK, details="All good", value=100)
        self.assertEqual(result.status, ValueStatus.OK)
        self.assertEqual(result.details, "All good")
        self.assertEqual(result.value, 100)


class MockValidatedValue(ValidatedValue):

    @classmethod
    def validate(cls, validated_value) -> ValidatedResponse:
        if validated_value is None:
            return ValidatedResponse(status=ValueStatus.EXCEPTION, details="Invalid value", value=None)
        return ValidatedResponse(status=ValueStatus.OK, details="Valid value", value=validated_value)


class TestValidatedValue(unittest.TestCase):

    def test_validated_value_initialization_success(self):
        v = MockValidatedValue(100)
        self.assertEqual(v.value, 100)
        self.assertEqual(v.status, ValueStatus.OK)
        self.assertEqual(v.details, "Valid value")

    def test_validated_value_initialization_failure(self):
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

    def test_validated_value_validate_method(self):
        """Test the validate method directly."""
        valid_response = MockValidatedValue.validate(100)
        invalid_response = MockValidatedValue.validate(None)

        self.assertEqual(valid_response.status, ValueStatus.OK)
        self.assertEqual(valid_response.details, "Valid value")
        self.assertEqual(valid_response.value, 100)

        self.assertEqual(invalid_response.status, ValueStatus.EXCEPTION)
        self.assertEqual(invalid_response.details, "Invalid value")
        self.assertIsNone(invalid_response.value)


class MockStrictValidatedValue(StrictValidatedValue):

    @classmethod
    def validate(cls, validated_value) -> ValidatedResponse:
        if validated_value is None:
            return ValidatedResponse(status=ValueStatus.EXCEPTION, details="Invalid value", value=None)
        return ValidatedResponse(status=ValueStatus.OK, details="Valid value", value=validated_value)


class TestStrictValidatedValue(unittest.TestCase):

    def test_strict_validated_value_success(self):
        strict_v = MockStrictValidatedValue(100)
        self.assertEqual(strict_v.value, 100)
        self.assertEqual(strict_v.status, ValueStatus.OK)
        self.assertEqual(strict_v.details, "Valid value")

    def test_strict_validated_value_failure(self):
        with self.assertRaises(ValueError):
            MockStrictValidatedValue(None)  # Should raise ValueError immediately

    def test_strict_validated_value_validate_method(self):
        """Test the validate method directly for StrictValidatedValue."""
        valid_response = MockStrictValidatedValue.validate(100)
        invalid_response = MockStrictValidatedValue.validate(None)

        self.assertEqual(valid_response.status, ValueStatus.OK)
        self.assertEqual(valid_response.details, "Valid value")
        self.assertEqual(valid_response.value, 100)

        self.assertEqual(invalid_response.status, ValueStatus.EXCEPTION)
        self.assertEqual(invalid_response.details, "Invalid value")
        self.assertIsNone(invalid_response.value)


class MockRangeValidatedValue(RangeValidatedValue):
    valid_types = (int,)
    low_value = 0
    high_value = 100


class TestRangeValidatedValue(unittest.TestCase):

    def test_range_validated_value_within_range(self):
        v = MockRangeValidatedValue(50)
        self.assertEqual(v.value, 50)
        self.assertEqual(v.status, ValueStatus.OK)
        self.assertEqual(v.details, "")

    def test_range_validated_value_out_of_range(self):
        v = MockRangeValidatedValue(150)
        self.assertEqual(v.status, ValueStatus.EXCEPTION)
        with self.assertRaises(ValueError):
            _ = v.value  # Should raise ValueError since the value is out of range

    def test_range_validated_value_invalid_type(self):
        v = MockRangeValidatedValue("50")  # Invalid type
        self.assertEqual(v.status, ValueStatus.EXCEPTION)
        with self.assertRaises(ValueError):
            _ = v.value  # Should raise ValueError due to invalid type

    def test_range_validated_value_validate_method(self):
        """Test the validate method directly for RangeValidatedValue."""
        valid_response = MockRangeValidatedValue.validate(50)
        invalid_response = MockRangeValidatedValue.validate(150)
        invalid_type_response = MockRangeValidatedValue.validate("50")

        self.assertEqual(valid_response.status, ValueStatus.OK)
        self.assertEqual(valid_response.value, 50)

        self.assertEqual(invalid_response.status, ValueStatus.EXCEPTION)
        self.assertIsNone(invalid_response.value)

        self.assertEqual(invalid_type_response.status, ValueStatus.EXCEPTION)
        self.assertIsNone(invalid_type_response.value)


if __name__ == '__main__':
    unittest.main()
