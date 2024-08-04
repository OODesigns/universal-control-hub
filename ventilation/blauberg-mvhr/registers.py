from enum import Enum


class CoilRegister(Enum):
    CL_POWER = 0  # R/W Coils (1-bit registers) - modbus functions: 1, 5, 15
    CL_TIMER = 1  # R/W Unit On/Off
    CL_WEEK = 2  # R/W Main timer
    CL_BOOST_MODE = 3  # R Weekly Schedule
    CL_FPLC_MODE = 4  # R Boost mode
    CL_INT_RH_CTRL = 5  # R/W Fireplace mode
    CL_EXT_RH_CTRL = 6  # R/W Main humidity sensor activation
    CL_INT_CO2_CTRL = 7  # R/W External humidity sensor activation
    CL_EXT_CO2_CTRL = 8  # R/W Main CO2 sensor activation
    CL_INT_PM2_5_CTRL = 9  # R/W External CO2 sensor activation
    CL_EXT_PM2_5_CTRL = 10  # R/W Main PM2.5 sensor activation
    CL_INT_VOC_CTRL = 11  # R/W External PM2.5 sensor activation
    CL_EXT_VOC_CTRL = 12  # R/W Main VOC sensor activation
    CL_BOOST_SWITCH_CTRL = 13  # R/W External VOC sensor activation
    CL_FPLC_SWITCH_CTRL = 14  # R/W Input activation for the boost mode switch
    CL_FIRE_ALARM_CTRL = 15  # R/W Input activation for the fireplace mode switch
    CL_10V_SENSOR_CTRL = 16  # R/W Fire alarm sensor activation
    CL_RESET_FILTER_TIMER = 17  # W Input activation for the external control device 0-10 V
    CL_RESET_ALARM = 18  # W Reset timer countdown to filter replacement
    CL_RESTORE_FACTORY = 19  # W Reset all alarms
    CL_CLOUD_CTRL = 20  # R/W Restore everything to factory settings
    CL_MIN_SU_AIR_OUT_TEMP_CTRL = 21  # R/W Activation of control via cloud server
    CL_WATER_PRESS_CTRL = 22  # R/W Minimum room supply air temperature control
    CL_WATER_FLOW_CTRL = 23  # R/W Heat medium water pressure sensor activation
    CL_WATER_HEATER_AUTO_RESTART = 24  # R/W Heat medium water flow sensor activation


class DiscreteInputs(Enum):
    DI_CUR_BOOST_SWITCH = 0  # Current input status for the Boost mode switch
    DI_CUR_FPLC_SWITCH = 1  # Current input status for the Fireplace mode switch
    DI_CUR_FIRE_ALARM = 2  # Current status of the fire alarm sensor
    DI_STATUS_RH = 3  # Humidity setpoint excess indication
    DI_STATUS_CO2 = 4  # CO2 setpoint excess indication
    DI_STATUS_PM2_5 = 5  # PM2.5 setpoint excess indication
    DI_STATUS_VOC = 6  # VOC setpoint excess indication
    DI_STATUS_HEATER = 7  # Heater operation indication
    DI_STATUS_COOLER = 8  # Cooler operation indication
    DI_STATUS_FAN_BLOWING = 9  # Electric heater blowdown indication
    DI_CUR_PRE_HEATER_THERMOSTAT = 10  # Current input status for the preheating thermostat
    DI_CUR_MAIN_HEATER_THERMOSTAT = 11  # Current input status for the reheating thermostat
    DI_CUR_SU_FILTER_PRESS = 12  # Current input status for the differential pressure switch of the supply filter
    DI_CUR_EX_FILTER_PRESS = 13  # Current input status for the differential pressure switch of the extract filter
    DI_CUR_WATER_PRESS = 14  # Current status of the heat medium water pressure sensor
    DI_CUR_WATER_FLOW = 15  # Current status of the heat medium water flow sensor
    DI_CUR_SU_FAN_PRESS = 16  # Current input status for the differential pressure switch of the supply fan
    DI_CUR_EX_FAN_PRESS = 17  # Current input status for the differential pressure switch of the extract fan
    DI_WATER_PREHEATING_STATUS = 18  # Return water heating indicator before the air handling unit start-up
    DI_ALARM_CODE_0 = 19  # Alarm indicator with code No. 0
    DI_ALARM_CODE_1 = 20  # Alarm indicator with code No. 1
    DI_ALARM_CODE_2 = 21  # Alarm indicator with code No. 2
    DI_ALARM_CODE_3 = 22  # Alarm indicator with code No. 3
    DI_ALARM_CODE_4 = 23  # Alarm indicator with code No. 4
    DI_ALARM_CODE_5 = 24  # Alarm indicator with code No. 5
    DI_ALARM_CODE_6 = 25  # Alarm indicator with code No. 6
    DI_ALARM_CODE_7 = 26  # Alarm indicator with code No. 7
    DI_ALARM_CODE_8 = 27  # Alarm indicator with code No. 8
    DI_ALARM_CODE_9 = 28  # Alarm indicator with code No. 9
    DI_ALARM_CODE_10 = 29  # Alarm indicator with code No. 10
    DI_ALARM_CODE_11 = 30  # Alarm indicator with code No. 11
    DI_ALARM_CODE_12 = 31  # Alarm indicator with code No. 12
    DI_ALARM_CODE_13 = 32  # Alarm indicator with code No. 13
    DI_ALARM_CODE_14 = 33  # Alarm indicator with code No. 14
    DI_ALARM_CODE_15 = 34  # Alarm indicator with code No. 15
    DI_ALARM_CODE_16 = 35  # Alarm indicator with code No. 16
    DI_ALARM_CODE_17 = 36  # Alarm indicator with code No. 17
    DI_ALARM_CODE_18 = 37  # Alarm indicator with code No. 18
    DI_ALARM_CODE_19 = 38  # Alarm indicator with code No. 19
    DI_ALARM_CODE_20 = 39  # Alarm indicator with code No. 20
    DI_ALARM_CODE_21 = 40  # Alarm indicator with code No. 21
    DI_ALARM_CODE_22 = 41  # Alarm indicator with code No. 22
    DI_ALARM_CODE_23 = 42  # Alarm indicator with code No. 23
    DI_ALARM_CODE_24 = 43  # Alarm indicator with code No. 24
    DI_ALARM_CODE_25 = 44  # Alarm indicator with code No. 25
    DI_ALARM_CODE_26 = 45  # Alarm indicator with code No. 26
    DI_ALARM_CODE_27 = 46  # Alarm indicator with code No. 27
    DI_ALARM_CODE_28 = 47  # Alarm indicator with code No. 28
    DI_ALARM_CODE_29 = 48  # Alarm indicator with code No. 29
    DI_ALARM_CODE_30 = 49  # Alarm indicator with code No. 30
    DI_ALARM_CODE_31 = 50  # Alarm indicator with code No. 31
    DI_ALARM_CODE_32 = 51  # Alarm indicator with code No. 32
    DI_ALARM_CODE_33 = 52  # Alarm indicator with code No. 33
    DI_ALARM_CODE_34 = 53  # Alarm indicator with code No. 34
    DI_ALARM_CODE_35 = 54  # Alarm indicator with code No. 35
    DI_ALARM_CODE_36 = 55  # Alarm indicator with code No. 36
    DI_ALARM_CODE_37 = 56  # Alarm indicator with code No. 37
    DI_ALARM_CODE_38 = 57  # Alarm indicator with code No. 38
    DI_ALARM_CODE_39 = 58  # Alarm indicator with code No. 39
    DI_ALARM_CODE_40 = 59  # Alarm indicator with code No. 40
    DI_ALARM_CODE_41 = 60  # Alarm indicator with code No. 41
    DI_ALARM_CODE_42 = 61  # Alarm indicator with code No. 42
    DI_ALARM_CODE_43 = 62  # Alarm indicator with code No. 43
    DI_ALARM_CODE_44 = 63  # Alarm indicator with code No. 44
    DI_ALARM_CODE_45 = 64  # Alarm indicator with code No. 45
    DI_ALARM_CODE_46 = 65  # Alarm indicator with code No. 46
    DI_ALARM_CODE_47 = 66  # Alarm indicator with code No. 47
    DI_ALARM_CODE_48 = 67  # Alarm indicator with code No. 48
    DI_ALARM_CODE_49 = 68  # Alarm indicator with code No. 49
    DI_ALARM_CODE_50 = 69  # Alarm indicator with code No. 50
    DI_ALARM_CODE_51 = 70  # Alarm indicator with code No. 51
    DI_ALARM_CODE_52 = 71  # Alarm indicator with code No. 52


class InputRegisters(Enum):
    # Current temperature of the selected sensor, which controls the air temperature
    # Value 250 = 25.0 °C. -32768 - no sensor, +32767 - short circuit
    IR_CUR_SEL_TEMP = 0

    # Current temperature of the main outdoor air sensor before preheating
    # Value 250 = 25.0 °C. -32768 - no sensor, +32767 - short circuit
    IR_CURTEMP_SUAIR_IN = 1

    # Current temperature of the main supply air temperature sensor at the unit outlet downstream of the reheater
    # Value 250 = 25.0 °C. -32768 - no sensor, +32767 - short circuit
    IR_CURTEMP_SUAIR_OUT = 2

    # Current extract air temperature at the unit inlet
    # Value 250 = 25.0 °C. -32768 - no sensor, +32767 - short circuit
    IR_CURTEMP_EXAIR_IN = 3

    # Current exhaust air temperature at the unit outlet
    # Value 250 = 25.0 °C. -32768 - no sensor, +32767 - short circuit
    IR_CURTEMP_EXAIR_OUT = 4

    # Current temperature of the outdoor air temperature sensor (in the control panel, ...)
    # Value 250 = 25.0 °C. -32768 - no sensor, +32767 - short circuit
    IR_CURTEMP_EXT = 5

    # Return heat medium temperature
    # Value 250 = 25.0 °C. -32768 - no sensor, +32767 - short circuit
    IR_CURTEMP_WATER = 8

    # Current battery voltage for RTC
    IR_CURVBAT = 9

    # Current humidity of the main sensor. 0 – no sensor
    IR_CURRH_INT = 10

    # Current humidity of the outdoor sensor. 0 – no sensor
    IR_CURRH_EXT = 11

    # Current CO2 level of the main sensor. 0 – no sensor
    IR_CURCO2_INT = 12

    # Current CO2 level of the external sensor. 0 – no sensor
    IR_CURCO2_EXT = 13

    # Current PM2.5 level of the main sensor. 0 – no sensor
    IR_CURPM2_5_INT = 14

    # Current PM2.5 level of the external sensor. 0 – no sensor
    IR_CURPM2_5_EXT = 15

    # Current VOC level of the main sensor. 0 – no sensor
    IR_CURVOC_INT = 16

    # Current VOC level of the external sensor. 0 – no sensor
    IR_CURVOC_EXT = 17

    # Current value of the 0-10 V sensor
    IR_CUR10V_SENSOR = 18

    # Current supply air flow
    IR_CURSU_AIRFLOW = 19

    # Current exhaust air flow
    IR_CUREX_AIRFLOW = 20

    # Current pressure in the supply air duct
    IR_CURSU_PRESS = 21

    # Current pressure in the exhaust air duct
    IR_CUREX_PRESS = 22

    # Supply fan speed
    IR_SURPM = 23

    # Extract fan speed
    IR_EXRPM = 24

    # Current countdown time of the main timer
    IR_CURTIMER_TIME = 25

    # Countdown time of the filter replacement timer
    IR_CURFILTER_TIMER = 27

    # Motor hours
    IR_TOTALWORKINGTIME = 29

    # Filter condition:
    # 0 - clean, 1 - the intake supply filter is clogged, 2 - the extract filter is clogged,
    # 3 - both filters are clogged or the filter replacement timer has gone off (highest priority)
    IR_STATE_FILTER = 31

    # Current speed in Weekly schedule mode: 0 - Standby
    # 1 - Speed 1
    # 2 - Speed 2
    # 3 - Speed 3
    # 4 - Speed 4
    # 5 - Speed 5
    IR_CURWEEKSPEED = 32

    # Current temperature setpoint in Weekly schedule mode:
    # 0 - ventilation only, +15 ... + 30 °C
    IR_CURWEEKSETTEMP = 33

    # Firmware version
    # Firmware creation date
    IR_VERMAIN_FMW = 34

    # Device type (controller): 1 – S21
    IR_DEVICETYPE = 37

    # Alarm/warning indicator: 0 – no
    # 1 – alarm (highest priority)
    # 2 – warning
    IR_ALARM = 38

    # Control signal from the PID humidity controller
    IR_RH_U = 39

    # Control signal from the PID CO2 level controller
    IR_CO2_U = 40

    # Control signal from the PID PM2.5 level controller
    IR_PM2_5_U = 41

    # Control signal from the PID VOC level controller
    IR_VOC_U = 42

    # Control signal from the PID preheating controller
    IR_PREHEATER_U = 43

    # Control signal from the PID reheating controller
    IR_MAINHEATER_U = 44

    # Control signal from the PID bypass/rotary heat exchanger controller
    IR_BPS_ROTOR_U = 45

    # Control signal from the PID condenser unit controller
    IR_KKB_U = 46

    # Control signal from the PID return heat medium controller
    IR_RETURNWATER_U = 47

    # Temperature setpoint in the supply air duct. Calculated automatically
    # when the room sensor or the sensor in the exhaust air duct is selected.
    # Value 250 = 25.0 °C
    IR_SUAIR_OUTSETTEMP = 48

    # Return heat medium temperature setpoint during winter in Standby mode.
    # Calculated automatically depending on the outdoor temperature.
    # Value 250 = 25.0 °C
    IR_WATER_STANDBYSETTEMP = 49

    # Return heat medium temperature setpoint in winter before the air handling unit start-up.
    # Calculated automatically depending on the outdoor temperature.
    # Value 350 = 35.0 °C
    IR_WATER_STARTSETTEMP = 50
