import unittest
from devices.blauberg_temperature import BlaubergTemperature
from utils.value import ValueStatus

class TestBlaubergTemperature(unittest.TestCase):

    def test_valid_temperature(self):
        # Test with a valid Modbus value that should convert correctly to Celsius
        temp = BlaubergTemperature(250)  # This represents 25.0°C
        self.assertEqual(temp.value, 25.0)
        self.assertEqual(temp.status, ValueStatus.OK)
        self.assertEqual(temp.details, "")

        temp = BlaubergTemperature(300)  # This represents 30.0°C
        self.assertEqual(temp.value, 30.0)
        self.assertEqual(temp.status, ValueStatus.OK)
        self.assertEqual(temp.details, "")

    def test_no_sensor_detected(self):
        # Test the case where the sensor is not detected (-32768)
        temp = BlaubergTemperature(-32768)
        self.assertEqual(temp.status, ValueStatus.EXCEPTION)
        self.assertEqual(temp.details, "No sensor detected")
        with self.assertRaises(ValueError) as cm:
            _ = temp.value  # Should raise ValueError because there is no sensor detected
        self.assertEqual(str(cm.exception), "Cannot access value: No sensor detected")

    def test_short_circuit(self):
        # Test the case where there is a short circuit (+32767)
        temp = BlaubergTemperature(32767)
        self.assertEqual(temp.status, ValueStatus.EXCEPTION)
        self.assertEqual(temp.details, "Sensor short circuit")
        with self.assertRaises(ValueError) as cm:
            _ = temp.value  # Should raise ValueError because of a short circuit
        self.assertEqual(str(cm.exception), "Cannot access value: Sensor short circuit")

    def test_edge_case_low_temperature(self):
        # Test the lowest valid temperature value
        temp = BlaubergTemperature(-200)  # This represents -20.0°C
        self.assertEqual(temp.value, -20.0)
        self.assertEqual(temp.status, ValueStatus.OK)
        self.assertEqual(temp.details, "")

    def test_edge_case_high_temperature(self):
        # Test the highest valid temperature value
        temp = BlaubergTemperature(500)  # This represents 50.0°C
        self.assertEqual(temp.value, 50.0)
        self.assertEqual(temp.status, ValueStatus.OK)
        self.assertEqual(temp.details, "")

    def test_out_of_range_temperature(self):
        # Test a value that is within the valid Modbus range but outside the allowed temperature range
        temp = BlaubergTemperature(600)  # Represents 60.0°C, out of allowed range
        self.assertEqual(temp.status, ValueStatus.EXCEPTION)
        self.assertEqual(temp.details, "BlaubergTemperature must be a (<class 'int'>, <class 'float'>) between -20.0 and 50.0, got 60.0")
        with self.assertRaises(ValueError) as cm:
            _ = temp.value  # Should raise ValueError because temperature is out of range
        self.assertEqual(str(cm.exception), "Cannot access value: BlaubergTemperature must be a (<class 'int'>, <class 'float'>) between -20.0 and 50.0, got 60.0")

if __name__ == '__main__':
    unittest.main()
