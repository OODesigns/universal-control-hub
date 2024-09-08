from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from pymodbus import ModbusException
from pymodbus.client import ModbusBaseClient
from pymodbus.pdu import ExceptionResponse, ModbusResponse
from modbus.modbus_reader import ModbusResultAdapter
from utils.response import T, Response
from utils.status import Status


@dataclass(frozen=True)
class PyModbusBaseResult(ModbusResultAdapter[T], ABC):
    """Immutable base class for handling Modbus results using PyModbus."""
    _result: ModbusResponse = field(default=None, init=False)

    @classmethod
    async def create(cls, client: ModbusBaseClient, address: int, count: int):
        """Asynchronous factory method to create an instance and perform the read operation."""
        instance = cls()  # Create the instance
        object.__setattr__(instance, '_result', await instance.read(client, address, count))
        return instance

    @abstractmethod
    async def read(self, client: ModbusBaseClient, address: int, count: int) -> ModbusResponse: # pragma: no cover
        """Perform the Modbus read operation. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def get_data(self) -> List[T]: # pragma: no cover
        """Extract data from the ModbusResponse. Must be implemented by subclasses."""
        pass

    def is_error(self) -> bool:
        return isinstance(self._result, (ModbusException, ExceptionResponse)) or self._result.isError()

    def get_error_message(self) -> str:
        if isinstance(self._result, ModbusException):
            return f"ModbusException: {self._result}"
        if isinstance(self._result, ExceptionResponse):
            return f"Modbus exception response: {self._result}"
        if self._result.isError():
            return f"Modbus library error: {self._result}"
        return "Unknown error"

    def to_response(self) -> Response[T]:
        """Converts the PyModbusBaseResult to a ValidatedResult."""
        if self.is_error():
            return Response[T](
                status=Status.EXCEPTION,
                details=self.get_error_message(),
                value=None
            )
        else:
            return Response[T](
                status=Status.OK,
                details="Read successful",
                value=self.get_data()
            )

@dataclass(frozen=True)
class PyModbusBitResult(PyModbusBaseResult[List[bool]]):
    """Immutable class for handling the result of reading bits using PyModbus."""

    def get_data(self) -> List[bool]:
        return self._result.bits if not self.is_error() else []

    @abstractmethod
    async def read(self, client: ModbusBaseClient, address: int, count: int) -> ModbusResponse: # pragma: no cover
        """To be implemented in subclasses."""
        pass

@dataclass(frozen=True)
class PyModbusCoilResult(PyModbusBitResult):
    """Immutable class for handling the result of reading coils using PyModbus."""

    async def read(self, client: ModbusBaseClient, address: int, count: int) -> ModbusResponse:
        return await client.read_coils(address, count)

@dataclass(frozen=True)
class PyModbusDiscreteInputResult(PyModbusBitResult):
    """Immutable class for handling the result of reading discrete inputs using PyModbus."""

    async def read(self, client: ModbusBaseClient, address: int, count: int) -> ModbusResponse:
        return await client.read_discrete_inputs(address, count)

@dataclass(frozen=True)
class PyModbusRegisterResult(PyModbusBaseResult[List[int]]):
    """Immutable class for handling the result of reading registers using PyModbus."""

    def get_data(self) -> List[int]:
        return self._result.registers if not self.is_error() else []

    @abstractmethod
    async def read(self, client: ModbusBaseClient, address: int, count: int) -> ModbusResponse: # pragma: no cover
        """To be implemented in subclasses."""
        pass

@dataclass(frozen=True)
class PyModbusInputRegisterResult(PyModbusRegisterResult):
    """Immutable class for handling the result of reading input registers using PyModbus."""

    async def read(self, client: ModbusBaseClient, address: int, count: int) -> ModbusResponse:
        return await client.read_input_registers(address, count)

@dataclass(frozen=True)
class PyModbusHoldingRegisterResult(PyModbusRegisterResult):
    """Immutable class for handling the result of reading holding registers using PyModbus."""

    async def read(self, client: ModbusBaseClient, address: int, count: int) -> ModbusResponse:
        return await client.read_holding_registers(address, count)
