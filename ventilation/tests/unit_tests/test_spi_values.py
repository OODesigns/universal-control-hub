import unittest
from spi.spi_values import (SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz,
                            SPIMode, SPIBitsPerWord, SPIDataOrder, SPIFullDuplex, SPIIdleState)
from utils.value import ValueStatus


class TestSPIValues(unittest.TestCase):

    # Tests for SPIBusNumber
    def test_valid_spi_bus_number(self):
        bus_number = SPIBusNumber(1)
        self.assertEqual(bus_number.value, 1)
        self.assertEqual(bus_number.status, ValueStatus.OK)

    def test_invalid_spi_bus_number(self):
        bus_number = SPIBusNumber(8)  # Invalid, valid range is 0-7
        self.assertEqual(bus_number.status, ValueStatus.EXCEPTION)
        self.assertIsNone(bus_number._value)  # Since validation failed, value should be None
        self.assertIn('between 0 and 7', bus_number.details)

    # Tests for SPIChipSelect
    def test_valid_spi_chip_select(self):
        chip_select = SPIChipSelect(1)
        self.assertEqual(chip_select.value, 1)
        self.assertEqual(chip_select.status, ValueStatus.OK)

    def test_invalid_spi_chip_select(self):
        chip_select = SPIChipSelect(4)  # Invalid, valid range is 0-3
        self.assertEqual(chip_select.status, ValueStatus.EXCEPTION)
        self.assertIsNone(chip_select._value)
        self.assertIn('between 0 and 3', chip_select.details)

    # Tests for SPIMaxSpeedHz
    def test_valid_spi_max_speed(self):
        max_speed = SPIMaxSpeedHz(1000000)
        self.assertEqual(max_speed.value, 1000000)
        self.assertEqual(max_speed.status, ValueStatus.OK)

    def test_invalid_spi_max_speed(self):
        max_speed = SPIMaxSpeedHz(60000000)  # Invalid, valid range is 10kHz - 50MHz
        self.assertEqual(max_speed.status, ValueStatus.EXCEPTION)
        self.assertIsNone(max_speed._value)
        self.assertIn('between 10000 and 50000000', max_speed.details)

    # Tests for SPIMode
    def test_valid_spi_mode(self):
        spi_mode = SPIMode(0)
        self.assertEqual(spi_mode.value, 0)
        self.assertEqual(spi_mode.status, ValueStatus.OK)

    def test_invalid_spi_mode(self):
        spi_mode = SPIMode(4)  # Invalid, valid range is 0-3
        self.assertEqual(spi_mode.status, ValueStatus.EXCEPTION)
        self.assertIsNone(spi_mode._value)
        self.assertIn('between 0 and 3', spi_mode.details)

    # Tests for SPIBitsPerWord
    def test_valid_spi_bits_per_word(self):
        bits_per_word = SPIBitsPerWord(8)
        self.assertEqual(bits_per_word.value, 8)
        self.assertEqual(bits_per_word.status, ValueStatus.OK)

    def test_invalid_spi_bits_per_word(self):
        bits_per_word = SPIBitsPerWord(64)  # Invalid, valid range is 4-32
        self.assertEqual(bits_per_word.status, ValueStatus.EXCEPTION)
        self.assertIsNone(bits_per_word._value)
        self.assertIn('between 4 and 32', bits_per_word.details)

    # Tests for SPIDataOrder
    def test_valid_spi_data_order(self):
        data_order = SPIDataOrder('MSB')
        self.assertEqual(data_order.value, 'MSB')
        self.assertEqual(data_order.status, ValueStatus.OK)

    def test_invalid_spi_data_order(self):
        data_order = SPIDataOrder('XYZ')  # Invalid, must be 'MSB' or 'LSB'
        self.assertEqual(data_order.status, ValueStatus.EXCEPTION)
        self.assertIsNone(data_order._value)
        self.assertIn("'MSB' or 'LSB'", data_order.details)

    # Tests for SPIFullDuplex
    def test_valid_spi_full_duplex(self):
        full_duplex = SPIFullDuplex(True)
        self.assertEqual(full_duplex.value, True)
        self.assertEqual(full_duplex.status, ValueStatus.OK)

    def test_invalid_spi_full_duplex(self):
        full_duplex = SPIFullDuplex('NotABool')  # Invalid, must be a boolean
        self.assertEqual(full_duplex.status, ValueStatus.EXCEPTION)
        self.assertIsNone(full_duplex._value)
        self.assertIn('must be a boolean', full_duplex.details)

    # Tests for SPIIdleState
    def test_valid_spi_idle_state(self):
        idle_state = SPIIdleState('High')
        self.assertEqual(idle_state.value, 'High')
        self.assertEqual(idle_state.status, ValueStatus.OK)

    def test_invalid_spi_idle_state(self):
        idle_state = SPIIdleState('Middle')  # Invalid, must be 'High' or 'Low'
        self.assertEqual(idle_state.status, ValueStatus.EXCEPTION)
        self.assertIsNone(idle_state._value)
        self.assertIn("'High' or 'Low'", idle_state.details)

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
