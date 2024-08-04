from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import StartTcpServer
from registers import CoilRegister, DiscreteInputs, InputRegisters, HoldingRegister

SHIFT_BY_A_BYTE = 8

MIN_YEAR = 0

MIN_MONTH = 1

MIN_WEEK_DAY = 1

MIN_DAY = 1

ENUM_OFFSET: int = 1


def run_server():
    # Create data block with initial values based on the provided documentation
    coils = [0] * (max(coil.value for coil in CoilRegister) + ENUM_OFFSET)
    # Adding the minimum values or if there is a preset will use that based on documentation
    coils[CoilRegister.CL_RESET_FILTER_TIMER.value] = 1
    coils[CoilRegister.CL_RESET_ALARM.value] = 1
    coils[CoilRegister.CL_RESTORE_FACTORY.value] = 1
    coils[CoilRegister.CL_EXT_VOC_CTRL.value] = 1
    coils[CoilRegister.CL_FPLC_SWITCH_CTRL.value] = 1
    coils[CoilRegister.CL_MIN_SU_AIR_OUT_TEMP_CTRL.value] = 1
    coils[CoilRegister.CL_WATER_PRESS_CTRL.value] = 1
    coils[CoilRegister.CL_WATER_HEATER_AUTO_RESTART.value] = 1

    holding_register = [0] * (max(holding_register.value for holding_register in HoldingRegister) + ENUM_OFFSET)
    # Adding the minimum values or if there is a preset will use that based on documentation
    holding_register[HoldingRegister.HR_VENTILATION_MODE.value] = 1
    holding_register[HoldingRegister.HR_MAXSPEED_MODE.value] = 3
    holding_register[HoldingRegister.HR_SPEED_MODE.value] = 1
    holding_register[HoldingRegister.HR_MINSPEED.value] = 30
    holding_register[HoldingRegister.HR_MAXSPEED.value] = 100
    holding_register[HoldingRegister.HR_SUSPEED1.value] = 40
    holding_register[HoldingRegister.HR_EXSPEED1.value] = 40
    holding_register[HoldingRegister.HR_SUSPEED2.value] = 70
    holding_register[HoldingRegister.HR_EXSPEED2.value] = 70
    holding_register[HoldingRegister.HR_SUSPEED3.value] = 100
    holding_register[HoldingRegister.HR_EXSPEED3.value] = 100
    holding_register[HoldingRegister.HR_SUSPEED4.value] = 100
    holding_register[HoldingRegister.HR_EXSPEED4.value] = 100
    holding_register[HoldingRegister.HR_SUSPEED5.value] = 100
    holding_register[HoldingRegister.HR_EXSPEED5.value] = 100
    holding_register[HoldingRegister.HR_MANUALSPEED.value] = 50

    #TODO HR_BlowingSPEED onwards


    holding_register[HoldingRegister.HR_SETTEMP.value] = 15
    holding_register[HoldingRegister.HR_SETRH.value] = 40
    holding_register[HoldingRegister.HR_SETCO2.value] = 400
    holding_register[HoldingRegister.HR_SETPM2_5.value] = 100
    holding_register[HoldingRegister.HR_SETVOC.value] = 20
    holding_register[HoldingRegister.HR_SETTEMP_WINTERSUMMER.value] = 5
    holding_register[HoldingRegister.HR_MAXCO2_INT.value] = 500
    holding_register[HoldingRegister.HR_MAXPM2_5_INT.value] = 500
    holding_register[HoldingRegister.HR_SETMINSUAIR_OUTTEMP.value] = 5
    holding_register[HoldingRegister.HR_MAINHEATERMODE.value] = 1
    holding_register[HoldingRegister.HR_COOLERMODE.value] = 1
    holding_register[HoldingRegister.HR_PREHEATERMODE.value] = 1
    holding_register[HoldingRegister.HR_SETTIMEDETECTFANALARM.value] = 5
    holding_register[HoldingRegister.HR_SETTIMEFANBLOWING.value] = 20
    holding_register[HoldingRegister.HR_KKB_HYSTERESIS.value] = 1
    holding_register[HoldingRegister.HR_TIMEOPENBPS.value] = 2
    holding_register[HoldingRegister.HR_CORRTEMP_SUAIRIN.value] = -500
    holding_register[HoldingRegister.HR_CORRTEMP_SUAIR_OUT.value] = -500
    holding_register[HoldingRegister.HR_CORRTEMP_EXAIRIN.value] = -500
    holding_register[HoldingRegister.HR_CORRTEMP_EXAIR_OUT.value] = -500
    holding_register[HoldingRegister.HR_CORRTEMP_WATER.value] = -500
    holding_register[HoldingRegister.HR_CORRTEMP_EXT.value] = -500
    holding_register[HoldingRegister.HR_WATER_MAX_START_TIME.value] = 2
    holding_register[HoldingRegister.HR_WATER_MIN_START_TEMP.value] = 30
    holding_register[HoldingRegister.HR_WATER_MAX_START_TEMP.value] = 30
    holding_register[HoldingRegister.HR_WATER_MIN_ALARM_TEMP.value] = 10
    holding_register[HoldingRegister.HR_WATER_MAX_ALARM_TEMP.value] = 10

    # RTC_CALENDAR two dimensions where each dimension is a byte,
    # it means that the data is split into separate 8-bit (1-byte) values within
    # a single 16-bit register or across multiple registers.
    holding_register[HoldingRegister.HR_RTC_CALENDAR.value] = (MIN_DAY << SHIFT_BY_A_BYTE) | MIN_WEEK_DAY
    holding_register[HoldingRegister.HR_RTC_CALENDAR.value + ENUM_OFFSET] = (MIN_MONTH << SHIFT_BY_A_BYTE) | MIN_YEAR

    discrete_inputs = [0] * (max(discrete_inputs.value for discrete_inputs in DiscreteInputs) + ENUM_OFFSET)
    inputs_registers = [0] * (max(inputs_registers.value for inputs_registers in InputRegisters) + ENUM_OFFSET)

    store = ModbusSlaveContext(
        co=ModbusSequentialDataBlock(0, coils),
        di=ModbusSequentialDataBlock(0, discrete_inputs),  # Discrete Inputs (1 bit registers)
        hr=ModbusSequentialDataBlock(0, inputs_registers),  # Holding Registers (16 bit registers)
        ir=ModbusSequentialDataBlock(0, holding_register)  # Input Registers (16 bit registers)
    )

    context = ModbusServerContext(slaves=store, single=True)

    # Initialize the server information
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Blauberg'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'https://SomewhereNice.com/bashwork/blauberg.html/'
    identity.ProductName = 'Blauberg MVHR'
    identity.ModelName = 'MVHR 350'
    identity.MajorMinorRevision = '1.0'

    # Run the server
    #TODO How to set the context as it does not like it
    StartTcpServer(identity=identity, address=("localhost", 5020))


if __name__ == "__main__":
    run_server()
