from dataclasses import dataclass, field
from http.client import responses
from telnetlib import theNULL

from Demos.BackupRead_BackupWrite import readsize
from IPython.terminal.shortcuts.auto_suggest import accept, accept_and_keep_cursor
from lib2to3.btm_utils import tokens

from blauberg.blauberg_registers import InputRegisters
from blauberg.blauberg_temperature import BlaubergTemperature
from modbus.modbus import ModbusData
from mvhr_state import MVHRStateInterface
from utils.temperaturecelsius import TemperatureInterface

@dataclass(frozen=True)
class BlaubergMVHRState(MVHRStateInterface):
    data: ModbusData  # This is the input data passed to the class
    _temp_supply_out: TemperatureInterface = field(init=False)
    _temp_supply_in: TemperatureInterface = field(init=False)

    def __post_init__(self):
        # TODO I understand the issue temp is validate value which returns response when validating
        # this case I am not pro-gating the errors from the input_register etc into Blauberg temp
        # redo temp tokens accept the response passing in the EMU, that way if there are issue already
        # we can copy them, update test to show proto gation of errros

        # Also review Value to see if we can Generic[T] that and only have one type

        # Use object.__setattr__ to bypass the immutability in __post_init__
        object.__setattr__(self, '_temp_supply_out',
                           BlaubergTemperature(self.data.input_register.value[InputRegisters.IR_CURTEMP_SUAIR_OUT.value]))
        object.__setattr__(self, '_temp_supply_in',
                           BlaubergTemperature(self.data.input_register.value[InputRegisters.IR_CURTEMP_SUAIR_IN.value]))

    @property
    def temp_supply_out(self) -> TemperatureInterface:
        return self._temp_supply_out

    @property
    def temp_supply_in(self) -> TemperatureInterface:
        return self._temp_supply_in

