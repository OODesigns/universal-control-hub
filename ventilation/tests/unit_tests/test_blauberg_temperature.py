import unittest
from blauberg.blauberg_temperature import BlaubergTemperature, NO_SENSOR_DETECTED, SENSOR_SHORT_CIRCUIT
from utils.status import Status

class TestBlaubergTemperature(unittest.TestCase):

    def test_valid_temperature(self):
        # Test with a valid Modbus value that should convert correctly to Celsius
        data_array = [250, 300]  # Valid temperature data in Modbus registers
        temp = BlaubergTemperature(data_array, 0)  # 250 = 25.0°C
        self.assertEqual(temp.value, 25.0)
        self.assertEqual(temp.status, Status.OK)
        self.assertEqual(temp.details, "Validation successful")

        temp = BlaubergTemperature(data_array, 1)  # 300 = 30.0°C
        self.assertEqual(temp.value, 30.0)
        self.assertEqual(temp.status, Status.OK)
        self.assertEqual(temp.details, "Validation successful")

    def test_no_sensor_detected(self):
        # Test the case where the sensor is not detected (-32768)
        data_array = [NO_SENSOR_DETECTED, 300]  # Sensor not detected
        temp = BlaubergTemperature(data_array, 0)
        self.assertEqual(temp.status, Status.EXCEPTION)
        self.assertEqual(temp.details, "No sensor detected")
        self.assertIsNone(temp.value)

    def test_short_circuit(self):
        # Test the case where there is a short circuit (+32767)
        data_array = [SENSOR_SHORT_CIRCUIT, 300]  # Short circuit detected
        temp = BlaubergTemperature(data_array, 0)
        self.assertEqual(temp.status, Status.EXCEPTION)
        self.assertEqual(temp.details, "Sensor short circuit")
        self.assertIsNone(temp.value)

    def test_edge_case_low_temperature(self):
        # Test the lowest valid temperature value
        data_array = [-200, 500]  # -200 = -20.0°C
        temp = BlaubergTemperature(data_array, 0)
        self.assertEqual(temp.value, -20.0)
        self.assertEqual(temp.status, Status.OK)
        self.assertEqual(temp.details, "Validation successful")

    def test_edge_case_high_temperature(self):
        # Test the highest valid temperature value
        data_array = [500, 600]  # 500 = 50.0°C
        temp = BlaubergTemperature(data_array, 0)
        self.assertEqual(temp.value, 50.0)
        self.assertEqual(temp.status, Status.OK)
        self.assertEqual(temp.details, "Validation successful")

    def test_out_of_range_temperature(self):
        # Test a value that is within the valid Modbus range but outside the allowed temperature range
        data_array = [600, 500]  # 600 = 60.0°C, out of range
        temp = BlaubergTemperature(data_array, 0)
        self.assertEqual(temp.status, Status.EXCEPTION)
        self.assertEqual(temp.details, "Value must be less than or equal to 50.0, got 60.0")
        self.assertIsNone(temp.value)

    def test_invalid_register_selection(self):
        # Test the case where the register selected is not valid
        data_array = [250, 300]
        temp = BlaubergTemperature(data_array, 10)  # Invalid register
        self.assertEqual(temp.status, Status.EXCEPTION)
        self.assertEqual(temp.details, "Invalid temperature selection")
        self.assertIsNone(temp.value)

if __name__ == '__main__':
    unittest.main()
