from abc import ABC
from typing import Any, Callable, List
from utils.value import ValidatedResult, ValueStatus

class ModbusReader(ABC):
    def __init__(self, read_function: Callable[[int, int], Any], max_count: int):
        """
        Initialize the ModbusReadHelper.

        :param read_function: The function used to perform the Modbus read operation.
        :param max_count: The maximum number of items that can be read in a single Modbus request.
        """
        self.read_function = read_function
        self.max_count = max_count

    async def read(self, address: int, count: int) -> ValidatedResult:
        """
        Read the specified number of items starting at the given address.

        :param address: The starting address for the read operation.
        :param count: The total number of items to read.
        :return: A ValidatedResult object containing the status and read data.
        """
        results = []

        while count > 0:
            current_count = min(count, self.max_count)

            try:
                result = await self.read_function(address, current_count)
                if result is None:
                    return ValidatedResult(
                        status=ValueStatus.EXCEPTION,
                        details=f"Error reading from address {address}",
                        value=None
                    )
                results.extend(result)
                address += current_count
                count -= current_count

            except Exception as e:
                return ValidatedResult(
                    status=ValueStatus.EXCEPTION,
                    details=f"Exception occurred: {str(e)}",
                    value=None
                )

        return ValidatedResult(status=ValueStatus.OK, details="", value=results)


class ModbusBitReader(ModbusReader):
    def __init__(self, read_function: Callable[[int, int], List[bool]], max_count: int = 2000):
        super().__init__(read_function, max_count)

class ModbusWordReader(ModbusReader):
    def __init__(self, read_function: Callable[[int, int], List[int]], max_count: int = 125):
        super().__init__(read_function, max_count)