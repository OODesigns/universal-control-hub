import unittest
from typing import List
from unittest.mock import AsyncMock
from modbus.modbus_reader import ModbusBitReader, ModbusWordReader, ModbusResultAdapter
from utils.response import Response
from utils.status import Status


class MockModbusResultAdapter(ModbusResultAdapter[List[bool]]):
    def __init__(self, data=None, error=False):
        self._data = data
        self._error = error

    async def read(self, client, address: int, count: int):
        return self

    def is_error(self) -> bool:
        return self._error

    def get_data(self) -> List[bool]:
        return self._data

    def get_error_message(self) -> str:
        return "Simulated error" if self._error else ""

    def to_response(self) -> Response[List[bool]]:
        if self._error:
            return Response[List[bool]](
                status=Status.EXCEPTION,
                details=self.get_error_message(),
                value=None
            )
        return Response[List[bool]](
            status=Status.OK,
            details="Read successful",
            value=self._data
        )

class TestModbusBitReader(unittest.IsolatedAsyncioTestCase):

    async def test_read_bits_single_chunk(self):
        # Mock the read function to simulate a successful read with a ModbusResultAdapter
        mock_result_adapter = MockModbusResultAdapter(data=[True, False, True, False])
        mock_read_function = AsyncMock(return_value=mock_result_adapter)

        reader = ModbusBitReader(read_function=mock_read_function)
        result = await reader.read(0, 4)

        # Verify the result
        self.assertEqual(result.status, Status.OK)
        self.assertEqual(result.value, [True, False, True, False])

    async def test_read_bits_multiple_chunks(self):
        # Mock the read function to simulate successful reads in chunks
        # side_effect: This is an argument to AsyncMock that defines what the mocked function
        # should return each time it is called. It allows us to simulate the behavior of the
        # function across multiple calls:

        # First chunk: The first time the function is called, it returns a list of 2000 True values,
        # simulating a successful read of 2000 bits.
        # Second chunk: The second time the function is called, it returns a list of 500 False values,
        # simulating a successful read of the next 500 bits.
        mock_read_function = AsyncMock(side_effect=[
            MockModbusResultAdapter(data=[True] * 2000),  # First chunk
            MockModbusResultAdapter(data=[False] * 500)  # Second chunk
        ])

        reader = ModbusBitReader(read_function=mock_read_function)
        result = await reader.read(0, 2500)

        # Verify the result
        self.assertEqual(result.status, Status.OK)
        self.assertEqual(len(result.value), 2500)
        self.assertEqual(result.value[:2000], [True] * 2000)
        self.assertEqual(result.value[2000:], [False] * 500)

    async def test_read_bits_error(self):
        # Mock the read function to simulate an error using ModbusResultAdapter
        mock_result_adapter = MockModbusResultAdapter(error=True)
        mock_read_function = AsyncMock(return_value=mock_result_adapter)

        reader = ModbusBitReader(read_function=mock_read_function)
        result = await reader.read(0, 4)

        # Verify the result
        self.assertEqual(result.status, Status.EXCEPTION)
        self.assertIsNone(result.value)

class MockModbusWordResultAdapter(ModbusResultAdapter[List[int]]):
    def __init__(self, data=None, error=False):
        self._data = data
        self._error = error

    async def read(self, client, address: int, count: int):
        return self

    def is_error(self) -> bool:
        return self._error

    def get_data(self) -> List[int]:
        return self._data

    def get_error_message(self) -> str:
        return "Simulated error" if self._error else ""

    def to_response(self) -> Response[List[int]]:
        if self._error:
            return Response[List[int]](
                status=Status.EXCEPTION,
                details=self.get_error_message(),
                value=None
            )
        return Response[List[int]](
            status=Status.OK,
            details="Read successful",
            value=self._data
        )

class TestModbusWordReader(unittest.IsolatedAsyncioTestCase):

    async def test_read_words_single_chunk(self):
        # Mock the read function to simulate a successful read with a ModbusResultAdapter
        mock_result_adapter = MockModbusWordResultAdapter(data=[100, 200, 300, 400])
        mock_read_function = AsyncMock(return_value=mock_result_adapter)

        reader = ModbusWordReader(read_function=mock_read_function)
        result = await reader.read(0, 4)

        # Verify the result
        self.assertEqual(result.status, Status.OK)
        self.assertEqual(result.value, [100, 200, 300, 400])

    async def test_read_words_multiple_chunks(self):
        # Mock the read function to simulate successful reads in chunks

        # First chunk: The first time mock_read_function is called,
        # it will return a list with 125 items, each with the value 100.

        # Second chunk: The second time mock_read_function is called,
        # it will return a list with 100 items, each with the value 200.
        mock_read_function = AsyncMock(side_effect=[
            MockModbusWordResultAdapter(data=[100] * 125),  # First chunk
            MockModbusWordResultAdapter(data=[200] * 100)  # Second chunk
        ])

        reader = ModbusWordReader(read_function=mock_read_function)
        result = await reader.read(0, 225)

        # Verify the result
        self.assertEqual(result.status, Status.OK)
        self.assertEqual(len(result.value), 225)
        self.assertEqual(result.value[:125], [100] * 125)
        self.assertEqual(result.value[125:], [200] * 100)

    async def test_read_words_error(self):
        # Mock the read function to simulate an error using ModbusResultAdapter
        mock_result_adapter = MockModbusWordResultAdapter(error=True)
        mock_read_function = AsyncMock(return_value=mock_result_adapter)

        reader = ModbusWordReader(read_function=mock_read_function)
        result = await reader.read(0, 4)

        # Verify the result
        self.assertEqual(result.status, Status.EXCEPTION)
        self.assertIsNone(result.value)


if __name__ == '__main__':
    unittest.main()
