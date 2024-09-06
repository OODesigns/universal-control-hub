import unittest
from abc import ABC
from unittest.mock import MagicMock

from spi.spi import SPIInterface
from spi.spi_builder import SPIBuilder
from spi.spi_values import SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz, SPIMode, SPIBitsPerWord, SPIDataOrder, SPIFullDuplex, SPIIdleState


class MockSPIInterface(SPIInterface, ABC):
    pass


class TestSPIBuilder(unittest.TestCase):

    def test_set_bus(self):
        spi_builder = SPIBuilder(client_class=MockSPIInterface)
        bus = SPIBusNumber(1)
        spi_builder.set_bus(bus)
        self.assertEqual(spi_builder.bus, bus)

    def test_set_chip_select(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        device = SPIChipSelect(1)
        builder.set_chip_select(device)
        self.assertEqual(builder.chip_select, device)

    def test_set_max_speed_hz(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        max_speed_hz = SPIMaxSpeedHz(500000)
        builder.set_max_speed_hz(max_speed_hz)
        self.assertEqual(builder.max_speed_hz, max_speed_hz)

    def test_set_mode(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        mode = SPIMode(0)
        builder.set_mode(mode)
        self.assertEqual(builder.mode, mode)

    def test_set_bits_per_word(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        bits_per_word = SPIBitsPerWord(8)
        builder.set_bits_per_word(bits_per_word)
        self.assertEqual(builder.bits_per_word, bits_per_word)

    # New tests for SPIDataOrder
    def test_set_data_order(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        data_order = SPIDataOrder('MSB')
        builder.set_data_order(data_order)
        self.assertEqual(builder.data_order, data_order)

    # New tests for SPIFullDuplex
    def test_set_full_duplex(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        full_duplex = SPIFullDuplex(True)
        builder.set_full_duplex(full_duplex)
        self.assertEqual(builder.full_duplex, full_duplex)

    # New tests for SPIIdleState
    def test_set_idle_state(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        idle_state = SPIIdleState('High')
        builder.set_idle_state(idle_state)
        self.assertEqual(builder.idle_state, idle_state)

    def test_build_valid(self):
        mock = MagicMock(spec=MockSPIInterface)
        # noinspection PyTypeChecker
        builder = SPIBuilder(client_class=mock)
        builder.set_bus(SPIBusNumber(0)) \
            .set_chip_select(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8)) \
            .set_data_order(SPIDataOrder('MSB')) \
            .set_full_duplex(SPIFullDuplex(True)) \
            .set_idle_state(SPIIdleState('High'))

        # Build the SPI instance and ensure that the client class is called
        spi_instance = builder.build()
        mock.assert_called_once_with(builder)
        self.assertEqual(spi_instance, mock.return_value)

    def test_build_missing_bus(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        builder.set_chip_select(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8)) \
            .set_data_order(SPIDataOrder('MSB')) \
            .set_full_duplex(SPIFullDuplex(True)) \
            .set_idle_state(SPIIdleState('High'))

        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_device(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        builder.set_bus(SPIBusNumber(0)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8)) \
            .set_data_order(SPIDataOrder('MSB')) \
            .set_full_duplex(SPIFullDuplex(True)) \
            .set_idle_state(SPIIdleState('High'))

        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_max_speed(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        builder.set_bus(SPIBusNumber(0)) \
            .set_chip_select(SPIChipSelect(1)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8)) \
            .set_data_order(SPIDataOrder('MSB')) \
            .set_full_duplex(SPIFullDuplex(True)) \
            .set_idle_state(SPIIdleState('High'))

        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_mode(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        builder.set_bus(SPIBusNumber(0)) \
            .set_chip_select(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_bits_per_word(SPIBitsPerWord(8)) \
            .set_data_order(SPIDataOrder('MSB')) \
            .set_full_duplex(SPIFullDuplex(True)) \
            .set_idle_state(SPIIdleState('High'))

        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_bits_per_word(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        builder.set_bus(SPIBusNumber(0)) \
            .set_chip_select(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_data_order(SPIDataOrder('MSB')) \
            .set_full_duplex(SPIFullDuplex(True)) \
            .set_idle_state(SPIIdleState('High'))

        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_data_order(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        builder.set_bus(SPIBusNumber(0)) \
            .set_chip_select(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8)) \
            .set_full_duplex(SPIFullDuplex(True)) \
            .set_idle_state(SPIIdleState('High'))

        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_full_duplex(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        builder.set_bus(SPIBusNumber(0)) \
            .set_chip_select(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8)) \
            .set_data_order(SPIDataOrder('MSB')) \
            .set_idle_state(SPIIdleState('High'))

        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_idle_state(self):
        builder = SPIBuilder(client_class=MockSPIInterface)
        builder.set_bus(SPIBusNumber(0)) \
            .set_chip_select(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8)) \
            .set_data_order(SPIDataOrder('MSB')) \
            .set_full_duplex(SPIFullDuplex(True))

        with self.assertRaises(AssertionError):
            builder.build()

    def test_copy_builder(self):
        # Create the first builder with all values set
        builder1 = SPIBuilder(client_class=MockSPIInterface)
        builder1.set_bus(SPIBusNumber(1)) \
            .set_chip_select(SPIChipSelect(0)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8)) \
            .set_data_order(SPIDataOrder('MSB')) \
            .set_full_duplex(SPIFullDuplex(True)) \
            .set_idle_state(SPIIdleState('High'))

        # Create a new builder by passing the first builder
        builder2 = SPIBuilder(builder=builder1, client_class=MockSPIInterface)

        # Assert that all values are copied correctly
        self.assertEqual(builder2.bus, builder1.bus)
        self.assertEqual(builder2.chip_select, builder1.chip_select)
        self.assertEqual(builder2.max_speed_hz, builder1.max_speed_hz)
        self.assertEqual(builder2.mode, builder1.mode)
        self.assertEqual(builder2.bits_per_word, builder1.bits_per_word)
        self.assertEqual(builder2.data_order, builder1.data_order)
        self.assertEqual(builder2.full_duplex, builder1.full_duplex)
        self.assertEqual(builder2.idle_state, builder1.idle_state)

