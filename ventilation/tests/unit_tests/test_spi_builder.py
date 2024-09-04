import unittest
from abc import ABC
from unittest.mock import MagicMock

from spi.spi import SPIInterface
from spi.spi_builder import SPIBuilder
from spi.spi_values import SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz, SPIMode, SPIBitsPerWord


class MockSPIInterface(SPIInterface, ABC):
    pass


class TestSPIBuilder(unittest.TestCase):
    pass

    def test_set_bus(self):
        spi_builder = SPIBuilder(client_class=MockSPIInterface)
        bus = SPIBusNumber(1)
        spi_builder.set_bus(bus)
        self.assertEqual(spi_builder.bus, bus)

    def test_set_device(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        device = SPIChipSelect(1)  # Example device value
        builder.set_device(device)
        self.assertEqual(builder.device, device)

    def test_set_max_speed_hz(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        max_speed_hz = SPIMaxSpeedHz(500000)  # Example max speed value
        builder.set_max_speed_hz(max_speed_hz)
        self.assertEqual(builder.max_speed_hz, max_speed_hz)

    def test_set_mode(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        mode = SPIMode(0)  # Example mode value
        builder.set_mode(mode)
        self.assertEqual(builder.mode, mode)

    def test_set_bits_per_word(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        bits_per_word = SPIBitsPerWord(8)  # Example bits per word value
        builder.set_bits_per_word(bits_per_word)
        self.assertEqual(builder.bits_per_word, bits_per_word)

    def test_build_valid(self):
        mock = MagicMock(spec=MockSPIInterface)
        # noinspection PyTypeChecker
        builder = SPIBuilder(client_class=mock)
        builder.set_bus(SPIBusNumber(0)) \
            .set_device(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8))

        # Build the SPI instance and ensure that the client class is called
        spi_instance = builder.build()
        mock.assert_called_once_with(builder)
        self.assertEqual(spi_instance, mock.return_value)

    def test_build_missing_bus(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        builder.set_device(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8))

        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_device(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        builder.set_bus(SPIBusNumber(0)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8))

        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_max_speed(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        builder.set_bus(SPIBusNumber(0)) \
            .set_device(SPIChipSelect(1)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8))

        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_mode(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        builder.set_bus(SPIBusNumber(0)) \
            .set_device(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_bits_per_word(SPIBitsPerWord(8))

        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_bits_per_word(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        builder.set_bus(SPIBusNumber(0)) \
            .set_device(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0))

        with self.assertRaises(AssertionError):
            builder.build()