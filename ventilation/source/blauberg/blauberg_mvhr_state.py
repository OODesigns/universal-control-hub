from dataclasses import dataclass, field
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
        # Use object.__setattr__ to bypass the immutability in __post_init__
        object.__setattr__(self, '_temp_supply_out',
                           BlaubergTemperature(self.data.input_register[InputRegisters.IR_CURTEMP_SUAIR_OUT.value]))
        object.__setattr__(self, '_temp_supply_in',
                           BlaubergTemperature(self.data.input_register[InputRegisters.IR_CURTEMP_SUAIR_IN.value]))

    @property
    def temp_supply_out(self) -> TemperatureInterface:
        return self._temp_supply_out

    @property
    def temp_supply_in(self) -> TemperatureInterface:
        return self._temp_supply_in
