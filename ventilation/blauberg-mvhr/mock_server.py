import logging

from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import StartTcpServer
from registers import CoilRegister, DiscreteInputs, InputRegisters, HoldingRegister

MAX_BYTE_VALUE = 255

ASCII_SYMBOL_1 = 49

DIM_2 = 1

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
    holding_register[HoldingRegister.HR_BLOWINGSPEED.value] = 50
    holding_register[HoldingRegister.HR_BOOST_SUSPEED.value] = 100
    holding_register[HoldingRegister.HR_BOOST_EXSPEED.value] = 100
    holding_register[HoldingRegister.HR_FPLC_SUSPEED.value] = 60
    holding_register[HoldingRegister.HR_FPLC_EXSPEED.value] = 60
    holding_register[HoldingRegister.HR_OPERATION_MODE.value] = 3
    holding_register[HoldingRegister.HR_SETTEMP.value] = 23
    holding_register[HoldingRegister.HR_SETRH.value] = 60
    holding_register[HoldingRegister.HR_SETCO2.value] = 1200
    holding_register[HoldingRegister.HR_SETPM2_5.value] = 400
    holding_register[HoldingRegister.HR_SETVOC.value] = 40
    holding_register[HoldingRegister.HR_TIMER_MODE.value] = 1
    holding_register[HoldingRegister.HR_SETTIMER_TEMP.value] = 23
    holding_register[HoldingRegister.HR_SETTIMER_TIME.value] = 30
    holding_register[HoldingRegister.HR_SETTEMP_WINTERSUMMER.value] = 7
    holding_register[HoldingRegister.HR_SELTEMP_SENSOR.value] = 2
    holding_register[HoldingRegister.HR_SETFILTER_TIMER.value] = 90
    holding_register[HoldingRegister.HR_MAXCO2_INT.value] = 2000
    holding_register[HoldingRegister.HR_MAXPM2_5_INT.value] = 1000
    holding_register[HoldingRegister.HR_SETMINSUAIR_OUTTEMP.value] = 10
    holding_register[HoldingRegister.HR_MAINHEATERMODE.value] = 2
    holding_register[HoldingRegister.HR_COOLERMODE.value] = 2
    holding_register[HoldingRegister.HR_PREHEATERMODE.value] = 2
    holding_register[HoldingRegister.HR_SETPREHEATERMANUAL.value] = 50
    holding_register[HoldingRegister.HR_SETBPSROTOR_MANUAL.value] = 100
    holding_register[HoldingRegister.HR_RH_KP.value] = 150
    holding_register[HoldingRegister.HR_RH_KI.value] = 150
    holding_register[HoldingRegister.HR_CO2_KP.value] = 150
    holding_register[HoldingRegister.HR_CO2_KI.value] = 150
    holding_register[HoldingRegister.HR_PM2_5_KP.value] = 150
    holding_register[HoldingRegister.HR_PM2_5_KI.value] = 150
    holding_register[HoldingRegister.HR_VOC_KP.value] = 150
    holding_register[HoldingRegister.HR_VOC_KI.value] = 150
    holding_register[HoldingRegister.HR_PREHEATER_KP.value] = 200
    holding_register[HoldingRegister.HR_PREHEATER_KI.value] = 200
    holding_register[HoldingRegister.HR_PREHEATER_KD.value] = 500
    holding_register[HoldingRegister.HR_MAINHEATER_KP.value] = 400
    holding_register[HoldingRegister.HR_MAINHEATER_KI.value] = 400
    holding_register[HoldingRegister.HR_MAINHEATER_KP.value] = 600
    holding_register[HoldingRegister.HR_BPS_ROTOR_KP.value] = 200
    holding_register[HoldingRegister.HR_BPS_ROTOR_KI.value] = 200
    holding_register[HoldingRegister.HR_BPS_ROTOR_KD.value] = 500
    holding_register[HoldingRegister.HR_KKB_KP.value] = 200
    holding_register[HoldingRegister.HR_KKB_KI.value] = 200
    holding_register[HoldingRegister.HR_KKB_KD.value] = 500
    holding_register[HoldingRegister.HR_RETURNWATER_KP.value] = 120
    holding_register[HoldingRegister.HR_RETURNWATER_KI.value] = 120
    holding_register[HoldingRegister.HR_RETURNWATER_KD.value] = 350
    holding_register[HoldingRegister.HR_FAN_ALARM_CTRL.value] = 2
    holding_register[HoldingRegister.HR_SETTIMEDETECTFANALARM.value] = 30
    holding_register[HoldingRegister.HR_SETTIMEFANBLOWING.value] = 120
    holding_register[HoldingRegister.HR_KKB_MINTIMEOFF.value] = 3
    holding_register[HoldingRegister.HR_KKB_MINTIMEON.value] = 1
    holding_register[HoldingRegister.HR_KKB_HYSTERESIS.value] = 2
    holding_register[HoldingRegister.HR_TIMEOPENBPS.value] = 2
    holding_register[HoldingRegister.HR_CORRTEMP_SUAIRIN.value] = 0
    holding_register[HoldingRegister.HR_CORRTEMP_SUAIR_OUT.value] = 0
    holding_register[HoldingRegister.HR_CORRTEMP_EXAIRIN.value] = 0
    holding_register[HoldingRegister.HR_CORRTEMP_EXAIR_OUT.value] = 0
    holding_register[HoldingRegister.HR_CORRTEMP_WATER.value] = 0
    holding_register[HoldingRegister.HR_CORRTEMP_EXT.value] = 0
    holding_register[HoldingRegister.HR_WATER_MAX_START_TIME.value] = 5
    holding_register[HoldingRegister.HR_WATER_MIN_START_TEMP.value] = 30
    holding_register[HoldingRegister.HR_WATER_MAX_START_TEMP.value] = 30
    holding_register[HoldingRegister.HR_WATER_MIN_ALARM_TEMP.value] = 12
    holding_register[HoldingRegister.HR_WATER_MAX_ALARM_TEMP.value] = 20
    # it means that the data is split into separate 8-bit (1-byte) values within
    # a single 16-bit register or across multiple registers.
    holding_register[HoldingRegister.HR_ENGINEER_PWD.value] = combine_bytes(ASCII_SYMBOL_1, ASCII_SYMBOL_1)
    holding_register[HoldingRegister.HR_ENGINEER_PWD.value + DIM_2] = combine_bytes(ASCII_SYMBOL_1, ASCII_SYMBOL_1)

    holding_register[HoldingRegister.HR_SETWEEK_MO_1ST_PERIOD_SPEED_TEMP.value] = combine_bytes(1, 23)
    holding_register[HoldingRegister.HR_SETWEEK_MO_1ST_PERIOD_END_HOURS_MINUTES.value] = combine_bytes(6, 0)
    holding_register[HoldingRegister.HR_SETWEEK_MO_2ND_PERIOD_SPEED_TEMP.value] = combine_bytes(1, 23)
    holding_register[HoldingRegister.HR_SETWEEK_MO_2ND_PERIOD_END_HOURS_MINUTES.value] = combine_bytes(9, 0)
    holding_register[HoldingRegister.HR_SETWEEK_MO_3RD_PERIOD_SPEED_TEMP.value] = combine_bytes(1, 23)
    holding_register[HoldingRegister.HR_SETWEEK_MO_3RD_PERIOD_END_HOURS_MINUTES.value] = combine_bytes(19, 0)
    holding_register[HoldingRegister.HR_SETWEEK_MO_4TH_PERIOD_SPEED_TEMP.value] = combine_bytes(1, 23)
    holding_register[HoldingRegister.HR_SETWEEK_MO_4TH_PERIOD_END.value] = combine_bytes(23, 59)

    # TODo other holding registers

    # RTC_CALENDAR two dimensions where each dimension is a byte,
    # it means that the data is split into separate 8-bit (1-byte) values within
    # a single 16-bit register or across multiple registers.
    holding_register[HoldingRegister.HR_RTC_CALENDAR.value] = (MIN_DAY << SHIFT_BY_A_BYTE) | MIN_WEEK_DAY
    holding_register[HoldingRegister.HR_RTC_CALENDAR.value + DIM_2] = (MIN_MONTH << SHIFT_BY_A_BYTE) | MIN_YEAR

    discrete_inputs = [0] * (max(discrete_inputs.value for discrete_inputs in DiscreteInputs) + ENUM_OFFSET)
    inputs_registers = [0] * (max(inputs_registers.value for inputs_registers in InputRegisters) + ENUM_OFFSET)

    store = ModbusSlaveContext(
        co=ModbusSequentialDataBlock(0, coils),
        di=ModbusSequentialDataBlock(0, discrete_inputs),  # Discrete Inputs (1 bit registers)
        hr=ModbusSequentialDataBlock(0, inputs_registers),  # Holding Registers (16 bit registers)
        ir=ModbusSequentialDataBlock(0, holding_register)  # Input Registers (16 bit registers)
    )

    # Initialize the server information
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Blauberg'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'https://SomewhereNice.com/bashwork/blauberg.html/'
    identity.ProductName = 'Blauberg MVHR'
    identity.ModelName = 'MVHR 350'
    identity.MajorMinorRevision = '1.0'

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Starting Modbus TCP Server...')
    # Run the server
    StartTcpServer(context=ModbusServerContext(slaves=store, single=True),
                   identity=identity,
                   address=("localhost", 5020))


def combine_bytes(high_byte: int, low_byte: int) -> int:
    """
    Combine two bytes into a 16-bit value.

    Args:
        high_byte (int): The high byte (8 bits).
        low_byte (int): The low byte (8 bits).

    Returns:
        int: The combined 16-bit value.
    """
    if not (0 <= high_byte <= MAX_BYTE_VALUE):
        raise ValueError("high_byte must be between 0 and 255")
    if not (0 <= low_byte <= MAX_BYTE_VALUE):
        raise ValueError("low_byte must be between 0 and 255")

    return (high_byte << SHIFT_BY_A_BYTE) | low_byte


if __name__ == "__main__":
    run_server()
