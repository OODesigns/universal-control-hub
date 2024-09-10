import unittest
from spi.spi_values import (
    SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz, SPIMode, SPIBitsPerWord,
    SPIDataOrder, SPIFullDuplex, SPIIdleState
)
from utils.status import Status

class TestSPIValues(unittest.TestCase):

    # Tests for SPIBusNumber
    def test_valid_spi_bus_number(self):
        bus_number = SPIBusNumber(1)
        self.assertEqual(bus_number.value, 1)
        self.assertEqual(bus_number.status, Status.OK)

    def test_invalid_spi_bus_number(self):
        bus_number = SPIBusNumber(8)  # Invalid, valid range is 0-7
        self.assertEqual(bus_number.status, Status.EXCEPTION)
        self.assertIsNone(bus_number.value)  # Since validation failed, value should be None
        self.assertIn('Value must be less than or equal to 7', bus_number.details)

    # Tests for SPIChipSelect
    def test_valid_spi_chip_select(self):
        chip_select = SPIChipSelect(1)
        self.assertEqual(chip_select.value, 1)
        self.assertEqual(chip_select.status, Status.OK)

    def test_invalid_spi_chip_select(self):
        chip_select = SPIChipSelect(4)  # Invalid, valid range is 0-3
        self.assertEqual(chip_select.status, Status.EXCEPTION)
        self.assertIsNone(chip_select.value)
        self.assertIn('Value must be less than or equal to 3', chip_select.details)

    # Tests for SPIMaxSpeedHz
    def test_valid_spi_max_speed(self):
        max_speed = SPIMaxSpeedHz(1000000)
        self.assertEqual(max_speed.value, 1000000)
        self.assertEqual(max_speed.status, Status.OK)

    def test_invalid_spi_max_speed(self):
        max_speed = SPIMaxSpeedHz(60000000)  # Invalid, valid range is 10kHz - 50MHz
        self.assertEqual(max_speed.status, Status.EXCEPTION)
        self.assertIsNone(max_speed.value)
        self.assertIn('Value must be less than or equal to 50000000', max_speed.details)

    # Tests for SPIMode
    def test_valid_spi_mode(self):
        spi_mode = SPIMode(0)
        self.assertEqual(spi_mode.value, 0)
        self.assertEqual(spi_mode.status, Status.OK)

    def test_invalid_spi_mode(self):
        spi_mode = SPIMode(4)  # Invalid, valid range is 0-3
        self.assertEqual(spi_mode.status, Status.EXCEPTION)
        self.assertIsNone(spi_mode.value)
        self.assertIn('Value must be less than or equal to 3', spi_mode.details)

    # Tests for SPIBitsPerWord
    def test_valid_spi_bits_per_word(self):
        bits_per_word = SPIBitsPerWord(8)
        self.assertEqual(bits_per_word.value, 8)
        self.assertEqual(bits_per_word.status, Status.OK)

    def test_invalid_spi_bits_per_word(self):
        bits_per_word = SPIBitsPerWord(64)  # Invalid, valid range is 4-32
        self.assertEqual(bits_per_word.status, Status.EXCEPTION)
        self.assertIsNone(bits_per_word.value)
        self.assertIn('Value must be less than or equal to 32', bits_per_word.details)

    # Tests for SPIDataOrder
    def test_valid_spi_data_order(self):
        data_order = SPIDataOrder('MSB')
        self.assertEqual(data_order.value, 'MSB')
        self.assertEqual(data_order.status, Status.OK)

    def test_invalid_spi_data_order(self):
        data_order = SPIDataOrder('XYZ')  # Invalid, must be 'MSB' or 'LSB'
        self.assertEqual(data_order.status, Status.EXCEPTION)
        self.assertIsNone(data_order.value)
        self.assertIn("Value must be one of ['MSB', 'LSB']", data_order.details)

    # Tests for SPIFullDuplex
    def test_valid_spi_full_duplex(self):
        full_duplex = SPIFullDuplex(True)
        self.assertEqual(full_duplex.value, True)
        self.assertEqual(full_duplex.status, Status.OK)

    def test_invalid_spi_full_duplex(self):
        # noinspection PyTypeChecker
        full_duplex = SPIFullDuplex('NotABool')  # Invalid, must be a boolean
        self.assertEqual(full_duplex.status, Status.EXCEPTION)
        self.assertIsNone(full_duplex.value)
        self.assertIn(full_duplex.details, "Value must be one of [True, False], got NotABool")

    # Tests for SPIIdleState
    def test_valid_spi_idle_state(self):
        idle_state = SPIIdleState('High')
        self.assertEqual(idle_state.value, 'High')
        self.assertEqual(idle_state.status, Status.OK)

    def test_invalid_spi_idle_state(self):
        idle_state = SPIIdleState('Middle')  # Invalid, must be 'High' or 'Low'
        self.assertEqual(idle_state.status, Status.EXCEPTION)
        self.assertIsNone(idle_state.value)
        self.assertIn("Value must be one of ['High', 'Low']", idle_state.details)

    # Test for equality (==) and comparison operators (<, <=)
    def test_value_comparisons(self):
        bus1 = SPIBusNumber(1)
        bus2 = SPIBusNumber(2)
        self.assertTrue(bus1 < bus2)
        self.assertTrue(bus1 <= bus2)
        self.assertTrue(bus1 != bus2)
        self.assertEqual(bus1, SPIBusNumber(1))


if __name__ == '__main__':
    unittest.main()
