import unittest
import utils.value

class TestValue(unittest.TestCase):

    def test_value_initialization(self):
        v = utils.value.Value(10)
        self.assertEqual(v.value, 10)

    def test_value_equality(self):
        v1 = utils.value.Value(10)
        v2 = utils.value.Value(10)
        v3 = utils.value.Value(20)
        self.assertTrue(v1 == v2)
        self.assertFalse(v1 == v3)

    def test_value_comparison(self):
        v1 = utils.value.Value(10)
        v2 = utils.value.Value(20)
        self.assertTrue(v1 < v2)
        self.assertTrue(v1 <= v2)
        self.assertFalse(v2 < v1)
        self.assertFalse(v2 <= v1)

    def test_value_invalid_comparison(self):
        v1 = utils.value.Value(10)
        self.assertFalse(v1 == 10)

class TestValidatedResult(unittest.TestCase):

    def test_validated_result_initialization(self):
        result = utils.value.ValidatedResult(status=utils.value.ValueStatus.OK, details="All good", value=100)
        self.assertEqual(result.status, utils.value.ValueStatus.OK)
        self.assertEqual(result.details, "All good")
        self.assertEqual(result.value, 100)

class MockValidatedValue(utils.value.ValidatedValue):

    @classmethod
    def validate(cls, validated_value) -> utils.value.ValidatedResult:
        if validated_value is None:
            return utils.value.ValidatedResult(status=utils.value.ValueStatus.EXCEPTION, details="Invalid value", value=None)
        return utils.value.ValidatedResult(status=utils.value.ValueStatus.OK, details="Valid value", value=validated_value)

class TestValidatedValue(unittest.TestCase):

    def test_validated_value_success(self):
        v = MockValidatedValue(100)
        self.assertEqual(v.value, 100)
        self.assertEqual(v.status, utils.value.ValueStatus.OK)
        self.assertEqual(v.details, "Valid value")

    def test_validated_value_failure(self):
        v = MockValidatedValue(None)
        self.assertEqual(v.status, utils.value.ValueStatus.EXCEPTION)
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

class MockStrictValidatedValue(utils.value.StrictValidatedValue):
    @classmethod
    def validate(cls, validated_value) -> utils.value.ValidatedResult:
        if validated_value is None:
            return utils.value.ValidatedResult(status=utils.value.ValueStatus.EXCEPTION, details="Invalid value", value=None)
        return utils.value.ValidatedResult(status=utils.value.ValueStatus.OK, details="Valid value", value=validated_value)

class TestStrictValidatedValue(unittest.TestCase):

    def test_strict_validated_value_success(self):
        strict_v = MockStrictValidatedValue(100)
        self.assertEqual(strict_v.value, 100)
        self.assertEqual(strict_v.status, utils.value.ValueStatus.OK)
        self.assertEqual(strict_v.details, "Valid value")

    def test_strict_validated_value_failure(self):
        with self.assertRaises(ValueError):
            MockStrictValidatedValue(None)  # Should raise ValueError immediately

class MockRangeValidatedValue(utils.value.RangeValidatedValue):
    valid_types = (int,)
    low_value = 0
    high_value = 100

class TestRangeValidatedValue(unittest.TestCase):

    def test_range_validated_value_success(self):
        v = MockRangeValidatedValue(50)
        self.assertEqual(v.value, 50)
        self.assertEqual(v.status, utils.value.ValueStatus.OK)
        self.assertEqual(v.details, "")

    def test_range_validated_value_out_of_range(self):
        v = MockRangeValidatedValue(150)
        self.assertEqual(v.status, utils.value.ValueStatus.EXCEPTION)
        with self.assertRaises(ValueError):
            _ = v.value  # Should raise ValueError since the value is out of range

    def test_range_validated_value_invalid_type(self):
        v = MockRangeValidatedValue("50")  # Invalid type
        self.assertEqual(v.status, utils.value.ValueStatus.EXCEPTION)
        with self.assertRaises(ValueError):
            _ = v.value  # Should raise ValueError due to invalid type


if __name__ == '__main__':
    unittest.main()
