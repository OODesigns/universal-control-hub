import unittest
from unittest.mock import AsyncMock

from modbus.modbus_reader import ModbusBitReader, ModbusWordReader
from utils.value import ValueStatus


class TestModbusBitReader(unittest.IsolatedAsyncioTestCase):

    async def test_read_bits_single_chunk(self):
        # Mock the read function to simulate a successful read
        mock_read_function = AsyncMock(return_value=[True, False, True, False])

        reader = ModbusBitReader(read_function=mock_read_function)
        result = await reader.read(0, 4)

        # Verify the result
        self.assertEqual(result.status, ValueStatus.OK)
        self.assertEqual(result.value, [True, False, True, False])

    async def test_read_bits_multiple_chunks(self):
        # Mock the read function to simulate successful reads in chunks
        mock_read_function = AsyncMock(side_effect=[
            [True] * 2000,  # First chunk
            [False] * 500   # Second chunk
        ])

        reader = ModbusBitReader(read_function=mock_read_function)
        result = await reader.read(0, 2500)

        # Verify the result
        self.assertEqual(result.status, ValueStatus.OK)
        self.assertEqual(len(result.value), 2500)
        self.assertEqual(result.value[:2000], [True] * 2000)
        self.assertEqual(result.value[2000:], [False] * 500)

    async def test_read_bits_error(self):
        # Mock the read function to simulate an error
        mock_read_function = AsyncMock(return_value=None)

        reader = ModbusBitReader(read_function=mock_read_function)
        result = await reader.read(0, 4)

        # Verify the result
        self.assertEqual(result.status, ValueStatus.EXCEPTION)
        self.assertIsNone(result.value)

class TestModbusWordReader(unittest.IsolatedAsyncioTestCase):

    async def test_read_words_single_chunk(self):
        # Mock the read function to simulate a successful read
        mock_read_function = AsyncMock(return_value=[100, 200, 300, 400])

        reader = ModbusWordReader(read_function=mock_read_function)
        result = await reader.read(0, 4)

        # Verify the result
        self.assertEqual(result.status, ValueStatus.OK)
        self.assertEqual(result.value, [100, 200, 300, 400])

    async def test_read_words_multiple_chunks(self):
        # Mock the read function to simulate successful reads in chunks
        mock_read_function = AsyncMock(side_effect=[
            [100] * 125,  # First chunk
            [200] * 100   # Second chunk
        ])

        reader = ModbusWordReader(read_function=mock_read_function)
        result = await reader.read(0, 225)

        # Verify the result
        self.assertEqual(result.status, ValueStatus.OK)
        self.assertEqual(len(result.value), 225)
        self.assertEqual(result.value[:125], [100] * 125)
        self.assertEqual(result.value[125:], [200] * 100)

    async def test_read_words_error(self):
        # Mock the read function to simulate an error
        mock_read_function = AsyncMock(return_value=None)

        reader = ModbusWordReader(read_function=mock_read_function)
        result = await reader.read(0, 4)

        # Verify the result
        self.assertEqual(result.status, ValueStatus.EXCEPTION)
        self.assertIsNone(result.value)

