from abc import ABC, abstractmethod
from typing import Callable, List, Awaitable, Generic
from utils.response import T, Response
from utils.status import Status


class ModbusResultAdapter(Generic[T], ABC):
    @abstractmethod
    async def read(self, client, address: int, count: int):# pragma: no cover
        """Performs the Modbus read operation asynchronously."""
        pass

    @abstractmethod
    def is_error(self) -> bool:# pragma: no cover
        """Indicates if there was an error in the operation."""
        pass

    @abstractmethod
    def get_data(self) -> List[T]:# pragma: no cover
        """Returns the data from the Modbus operation."""
        pass

    @abstractmethod
    def get_error_message(self) -> str:# pragma: no cover
        """Returns the error message if there was an error."""
        pass

    @abstractmethod
    def to_response(self) -> Response[T]:# pragma: no cover
        """Converts the ModbusResultAdapter to a ValidatedResult."""
        pass

class ModbusReader(Generic[T]):
    def __init__(self, read_function: Callable[[int, int], Awaitable[ModbusResultAdapter[T]]], max_count: int):
        """
        Initialize the ModbusReader.

        :param read_function: The function used to perform the Modbus read operation.
        :param max_count: The maximum number of items that can be read in a single Modbus request.
        """
        self.read_function = read_function
        self.max_count = max_count

    async def read(self, start_address: int, total_count: int) -> Response[T]:
        """
        Read the specified number of items starting at the given address.

        :param start_address: The starting address for the read operation.
        :param total_count: The total number of items to read.
        :return: A ValidatedResult object containing the status and read data.
        """
        results = []
        current_address = start_address
        remaining_count = total_count

        while remaining_count > 0:
            current_count = min(self.max_count, remaining_count)
            result_adapter = await self.read_function(current_address, current_count)
            response = result_adapter.to_response()

            if response.status == Status.EXCEPTION:
                return response  # Return early if any error occurs

            results.extend(response.value)
            current_address += current_count
            remaining_count -= current_count

        return Response[T](
            status=Status.OK,
            details="Read successful",
            value=results
        )


class ModbusBitReader(ModbusReader[List[bool]]):
    def __init__(self, read_function: Callable[[int, int], Awaitable[ModbusResultAdapter[List[bool]]]], max_count: int = 2000):
        super().__init__(read_function, max_count)

class ModbusWordReader(ModbusReader[List[int]]):
    def __init__(self, read_function: Callable[[int, int], Awaitable[ModbusResultAdapter[List[int]]]], max_count: int = 125):
        super().__init__(read_function, max_count)
