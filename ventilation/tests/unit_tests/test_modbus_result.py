import unittest
from unittest.mock import AsyncMock, create_autospec

from pymodbus import ModbusException
from pymodbus.pdu import ModbusResponse, ExceptionResponse

from py_modbus.modbus_result import PyModbusCoilResult, PyModbusDiscreteInputResult, PyModbusInputRegisterResult, \
    PyModbusHoldingRegisterResult
from utils.value import ValueStatus


class TestPyModbusCoilResult(unittest.IsolatedAsyncioTestCase):

    async def test_read_coils_success(self):
        mock_client = AsyncMock()
        mock_response = create_autospec(ModbusResponse, instance=True)
        mock_response.bits = [True, False, True]
        mock_response.isError.return_value = False
        mock_client.read_coils.return_value = mock_response

        result = await PyModbusCoilResult.create(mock_client, address=1, count=3)
        self.assertFalse(result.is_error())
        self.assertEqual(result.get_data(), [True, False, True])
        self.assertEqual(result.to_validated_result().status, ValueStatus.OK)

    async def test_read_coils_error(self):
        mock_client = AsyncMock()
        mock_exception_response = create_autospec(ExceptionResponse, instance=True)
        mock_exception_response.isError.return_value = True
        mock_client.read_coils.return_value = mock_exception_response

        result = await PyModbusCoilResult.create(mock_client, address=1, count=3)
        self.assertEqual(result.get_data(), [])
        self.assertTrue(result.is_error())
        self.assertEqual(result.to_validated_result().status, ValueStatus.EXCEPTION)

    async def test_get_error_message_modbus_exception(self):
        mock_client = AsyncMock()
        mock_exception = create_autospec(ModbusException, instance=True)
        mock_client.read_coils.return_value = mock_exception

        result = await PyModbusCoilResult.create(mock_client, address=1, count=3)
        self.assertEqual(result.get_error_message(), f"ModbusException: {mock_exception}")

    async def test_get_error_message_exception_response(self):
        mock_client = AsyncMock()
        mock_exception_response = create_autospec(ExceptionResponse, instance=True)
        mock_client.read_coils.return_value = mock_exception_response

        result = await PyModbusCoilResult.create(mock_client, address=1, count=3)
        self.assertEqual(result.get_error_message(), f"Modbus exception response: {mock_exception_response}")

    async def test_get_error_message_is_error(self):
        mock_client = AsyncMock()
        mock_response = create_autospec(ModbusResponse, instance=True)
        mock_response.isError.return_value = True
        mock_client.read_coils.return_value = mock_response

        result = await PyModbusCoilResult.create(mock_client, address=1, count=3)
        self.assertEqual(result.get_error_message(), f"Modbus library error: {mock_response}")

    async def test_get_error_message_unknown_error(self):
        mock_client = AsyncMock()
        mock_response = create_autospec(ModbusResponse, instance=True)
        mock_response.isError.return_value = False
        mock_client.read_coils.return_value = mock_response

        result = await PyModbusCoilResult.create(mock_client, address=1, count=3)
        self.assertEqual(result.get_error_message(), "Unknown error")

class TestPyModbusDiscreteInputResult(unittest.IsolatedAsyncioTestCase):

    async def test_read_discrete_inputs_success(self):
        mock_client = AsyncMock()
        mock_response = create_autospec(ModbusResponse, instance=True)
        mock_response.isError.return_value = False
        mock_response.bits = [False, True, False]
        mock_client.read_discrete_inputs.return_value = mock_response

        result = await PyModbusDiscreteInputResult.create(mock_client, address=1, count=3)
        self.assertEqual(result.get_data(), [False, True, False])
        self.assertFalse(result.is_error())
        self.assertEqual(result.to_validated_result().status, ValueStatus.OK)

    async def test_read_discrete_inputs_error(self):
        mock_client = AsyncMock()
        mock_exception_response = create_autospec(ExceptionResponse, instance=True)
        mock_exception_response.isError.return_value = True
        mock_client.read_discrete_inputs.return_value = mock_exception_response

        result = await PyModbusDiscreteInputResult.create(mock_client, address=1, count=3)
        self.assertEqual(result.get_data(), [])
        self.assertTrue(result.is_error())
        self.assertEqual(result.to_validated_result().status, ValueStatus.EXCEPTION)

class TestPyModbusInputRegisterResult(unittest.IsolatedAsyncioTestCase):

    async def test_read_input_registers_success(self):
        mock_client = AsyncMock()
        mock_response = create_autospec(ModbusResponse, instance=True)
        mock_response.registers = [123, 456, 789]
        mock_response.isError.return_value = False
        mock_client.read_input_registers.return_value = mock_response

        result = await PyModbusInputRegisterResult.create(mock_client, address=1, count=3)
        self.assertEqual(result.get_data(), [123, 456, 789])
        self.assertFalse(result.is_error())
        self.assertEqual(result.to_validated_result().status, ValueStatus.OK)

    async def test_read_input_registers_error(self):
        mock_client = AsyncMock()
        mock_exception_response = create_autospec(ExceptionResponse, instance=True)
        mock_exception_response.isError.return_value = True
        mock_client.read_input_registers.return_value = mock_exception_response

        result = await PyModbusInputRegisterResult.create(mock_client, address=1, count=3)
        self.assertEqual(result.get_data(), [])
        self.assertTrue(result.is_error())
        self.assertEqual(result.to_validated_result().status, ValueStatus.EXCEPTION)

class TestPyModbusHoldingRegisterResult(unittest.IsolatedAsyncioTestCase):

    async def test_read_holding_registers_success(self):
        mock_client = AsyncMock()
        mock_response = create_autospec(ModbusResponse, instance=True)
        mock_response.registers = [321, 654, 987]
        mock_response.isError.return_value = False
        mock_client.read_holding_registers.return_value = mock_response

        result = await PyModbusHoldingRegisterResult.create(mock_client, address=1, count=3)
        self.assertEqual(result.get_data(), [321, 654, 987])
        self.assertFalse(result.is_error())
        self.assertEqual(result.to_validated_result().status, ValueStatus.OK)

    async def test_read_holding_registers_error(self):
        mock_client = AsyncMock()
        mock_exception_response = create_autospec(ExceptionResponse, instance=True)
        mock_exception_response.isError.return_value = True
        mock_client.read_holding_registers.return_value = mock_exception_response

        result = await PyModbusHoldingRegisterResult.create(mock_client, address=1, count=3)
        self.assertEqual(result.get_data(), [])
        self.assertTrue(result.is_error())
        self.assertEqual(result.to_validated_result().status, ValueStatus.EXCEPTION)

if __name__ == '__main__':
    unittest.main()
