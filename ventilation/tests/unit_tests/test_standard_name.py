import unittest

from utils.standard_name import StandardName
from utils.status import Status


class TestStandardName(unittest.TestCase):
    def test_valid_value(self):
        value = "abc_def"
        validated_value = StandardName(value)
        self.assertEqual(validated_value.status, Status.OK)
        self.assertEqual(validated_value.value, value)
        self.assertEqual(validated_value.details, "validation successful")

    def test_invalid_value_with_uppercase(self):
        value = "Abc_def"
        validated_value = StandardName(value)
        self.assertEqual(validated_value.status, Status.EXCEPTION)
        self.assertIsNone(validated_value.value)
        self.assertIn("Value must contain only lowercase letters", validated_value.details)

    def test_invalid_value_with_special_characters(self):
        value = "abc$def"
        validated_value = StandardName(value)
        self.assertEqual(validated_value.status, Status.EXCEPTION)
        self.assertIsNone(validated_value.value)
        self.assertIn("Value must contain only lowercase letters", validated_value.details)

    def test_invalid_value_with_numbers(self):
        value = "abc123"
        validated_value = StandardName(value)
        self.assertEqual(validated_value.status, Status.EXCEPTION)
        self.assertIsNone(validated_value.value)
        self.assertIn("Value must contain only lowercase letters", validated_value.details)