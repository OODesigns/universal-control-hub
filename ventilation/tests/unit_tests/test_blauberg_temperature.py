import unittest
from blauberg.blauberg_temperature import (BlaubergTemperature, NO_SENSOR_DETECTED,
                                           SENSOR_SHORT_CIRCUIT)
from utils.status import Status
from utils.value import Response

class TestBlaubergTemperature(unittest.TestCase):

    def test_valid_temperature(self):
        # Test with valid Modbus values that should convert correctly to Celsius
        valid_response = Response(status=Status.OK, details="Modbus read successful", value=[250, 300])

        # Validation happens automatically on instantiation
        temp = BlaubergTemperature(valid_response, 0)  # 250 = 25.0°C

        # Directly access the results
        self.assertEqual(temp.value, 25.0)
        self.assertEqual(temp.status, Status.OK)
        self.assertEqual(temp.details, "Validation successful")

        temp = BlaubergTemperature(valid_response, 1)  # 300 = 30.0°C
        self.assertEqual(temp.value, 30.0)
        self.assertEqual(temp.status, Status.OK)
        self.assertEqual(temp.details, "Validation successful")

    def test_no_sensor_detected(self):
        # Test the case where the sensor is not detected (-32768)
        sensor_error_response = Response(status=Status.OK, details="Modbus read successful", value=[NO_SENSOR_DETECTED, 300])
        temp = BlaubergTemperature(sensor_error_response, 0)

        self.assertEqual(temp.status, Status.EXCEPTION)
        self.assertEqual(temp.details, "No sensor detected")
        self.assertIsNone(temp.value)

    def test_sensor_short_circuit(self):
        # Test the case where there is a short circuit (+32767)
        short_circuit_response = Response(status=Status.OK, details="Modbus read successful", value=[SENSOR_SHORT_CIRCUIT, 300])
        temp = BlaubergTemperature(short_circuit_response, 0)

        self.assertEqual(temp.status, Status.EXCEPTION)
        self.assertEqual(temp.details, "Sensor short circuit")
        self.assertIsNone(temp.value)

    def test_edge_case_low_temperature(self):
        # Test the lowest valid temperature value
        valid_response = Response(status=Status.OK, details="Modbus read successful", value=[-200, 500])  # -200 = -20.0°C
        temp = BlaubergTemperature(valid_response, 0)

        self.assertEqual(temp.value, -20.0)
        self.assertEqual(temp.status, Status.OK)
        self.assertEqual(temp.details, "Validation successful")

    def test_edge_case_high_temperature(self):
        # Test the highest valid temperature value
        valid_response = Response(status=Status.OK, details="Modbus read successful", value=[500, 600])  # 500 = 50.0°C
        temp = BlaubergTemperature(valid_response, 0)

        self.assertEqual(temp.value, 50.0)
        self.assertEqual(temp.status, Status.OK)
        self.assertEqual(temp.details, "Validation successful")

    def test_out_of_range_temperature(self):
        # Test a value that is within the valid Modbus range but outside the allowed temperature range
        valid_response = Response(status=Status.OK, details="Modbus read successful", value=[600, 500])  # 600 = 60.0°C, out of range
        temp = BlaubergTemperature(valid_response, 0)

        self.assertEqual(temp.status, Status.EXCEPTION)
        self.assertEqual(temp.details, "Value must be less than or equal to 50.0, got 60.0")
        self.assertIsNone(temp.value)

    def test_invalid_register_selection(self):
        # Test the case where the register selected is not valid
        valid_response = Response(status=Status.OK, details="Modbus read successful", value=[250, 300])
        temp = BlaubergTemperature(valid_response, 10)  # Invalid register

        self.assertEqual(temp.status, Status.EXCEPTION)
        self.assertEqual("Invalid temperature selection", temp.details)
        self.assertIsNone(temp.value)

    def test_register_out_of_bounds(self):
        # Test register selection that is out of bounds in the data array
        valid_response = Response(status=Status.OK, details="Modbus read successful", value=[250, 300])
        temp = BlaubergTemperature(valid_response, 5)  # Out of bounds register index

        self.assertEqual(temp.status, Status.EXCEPTION)
        self.assertEqual("Register selection out of bounds of input register", temp.details)
        self.assertIsNone(temp.value)

    def test_chaining_of_strategies(self):
        # This tests the chaining between CustomSensorStrategy and ConversionStrategy
        valid_response = Response(status=Status.OK, details="Modbus read successful", value=[100, 400])  # Valid data for conversion
        temp = BlaubergTemperature(valid_response, 0)  # 100 = 10.0°C

        self.assertEqual(temp.value, 10.0)
        self.assertEqual(temp.status, Status.OK)
        self.assertEqual(temp.details, "Validation successful")

        temp = BlaubergTemperature(valid_response, 1)  # 400 = 40.0°C
        self.assertEqual(temp.value, 40.0)
        self.assertEqual(temp.status, Status.OK)
        self.assertEqual(temp.details, "Validation successful")

    def test_input_register_error_cascade(self):
        # Test where the input register returns an error, and the cascade stops further validation
        error_response = Response(status=Status.EXCEPTION, details="Modbus read failure", value=None)
        temp = BlaubergTemperature(error_response, 0)  # Using an invalid input register response

        self.assertEqual(temp.status, Status.EXCEPTION)
        self.assertEqual(temp.details, "Modbus read failure")
        self.assertIsNone(temp.value)

    def test_input_register_ok_cascade(self):
        # Test where the input register returns OK, and further strategies are executed
        valid_response = Response(status=Status.OK, details="Modbus read successful", value=[100, 200])
        temp = BlaubergTemperature(valid_response, 0)  # 100 = 10.0°C

        self.assertEqual(temp.status, Status.OK)
        self.assertEqual(temp.value, 10.0)  # Conversion should happen successfully
        self.assertEqual(temp.details, "Validation successful")

if __name__ == '__main__':
    unittest.main()
