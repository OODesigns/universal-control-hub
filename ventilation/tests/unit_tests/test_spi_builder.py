import unittest
from spi.spi_builder import SPIClientBuilder
from spi.spi_client import SPIClient
from spi.spi_values import SPIBusNumber, SPIChipSelect, SPIMaxSpeedHz, SPIMode, SPIBitsPerWord, SPIMSBDataOrder
from utils.response import Response
from utils.status import Status

class MockSPIClient(SPIClient):
    def __init__(self, builder):
        pass

    def open(self):
        pass

    def close(self):
        pass

    def execute(self, command=None):
        return Response(status=Status.OK, details="Mock execution", value=[0])

class TestSPIBuilder(unittest.TestCase):
    # Register the mock client class with the builder
    SPIClientBuilder.register_client(MockSPIClient)

    def test_set_bus(self):
        spi_builder = SPIClientBuilder()
        bus = SPIBusNumber(1)
        spi_builder.set_bus(bus)
        self.assertEqual(spi_builder.bus, bus)

    def test_set_chip_select(self):
        builder = SPIClientBuilder()
        device = SPIChipSelect(1)
        builder.set_chip_select(device)
        self.assertEqual(builder.chip_select, device)

    def test_set_max_speed_hz(self):
        builder = SPIClientBuilder()
        max_speed_hz = SPIMaxSpeedHz(500000)
        builder.set_max_speed_hz(max_speed_hz)
        self.assertEqual(builder.max_speed_hz, max_speed_hz)

    def test_set_mode(self):
        builder = SPIClientBuilder()
        mode = SPIMode(0)
        builder.set_mode(mode)
        self.assertEqual(builder.mode, mode)

    def test_set_bits_per_word(self):
        builder = SPIClientBuilder()
        bits_per_word = SPIBitsPerWord(8)
        builder.set_bits_per_word(bits_per_word)
        self.assertEqual(builder.bits_per_word, bits_per_word)

    # New tests for SPIDataOrder
    def test_set_data_order(self):
        builder = SPIClientBuilder()
        data_order = SPIMSBDataOrder(True)
        builder.set_data_order(data_order)
        self.assertEqual(builder.msb_data_order, data_order)

    def test_build_valid(self):
        # noinspection PyTypeChecker
        builder = SPIClientBuilder()
        builder.set_bus(SPIBusNumber(0)) \
            .set_chip_select(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8)) \
            .set_data_order(SPIMSBDataOrder(True))

        # Build the SPI instance and ensure that the client class is called
        spi_instance = builder.build()
        self.assertIsInstance(spi_instance, MockSPIClient)

    def test_build_missing_bus(self):
        builder = SPIClientBuilder()
        builder.set_chip_select(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8)) \
            .set_data_order(SPIMSBDataOrder(True))

        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_device(self):
        builder = SPIClientBuilder()
        builder.set_bus(SPIBusNumber(0)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8)) \
            .set_data_order(SPIMSBDataOrder(True))

        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_max_speed(self):
        builder = SPIClientBuilder()
        builder.set_bus(SPIBusNumber(0)) \
            .set_chip_select(SPIChipSelect(1)) \
            .set_mode(SPIMode(0)) \
            .set_bits_per_word(SPIBitsPerWord(8)) \
            .set_data_order(SPIMSBDataOrder(True))


        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_mode(self):
        builder = SPIClientBuilder()
        builder.set_bus(SPIBusNumber(0)) \
            .set_chip_select(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_bits_per_word(SPIBitsPerWord(8)) \
            .set_data_order(SPIMSBDataOrder(True))


        with self.assertRaises(AssertionError):
            builder.build()

    def test_build_missing_bits_per_word(self):
        builder = SPIClientBuilder()
        builder.set_bus(SPIBusNumber(0)) \
            .set_chip_select(SPIChipSelect(1)) \
            .set_max_speed_hz(SPIMaxSpeedHz(500000)) \
            .set_mode(SPIMode(0)) \
            .set_data_order(SPIMSBDataOrder(True))

        with self.assertRaises(AssertionError):
            builder.build()
