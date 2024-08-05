from enum import Enum


class CoilRegister(Enum):
    # R/W Coils (1-bit registers) - modbus functions: 1, 5, 15
    CL_POWER = 0
    # R/W Unit On/Off
    CL_TIMER = 1
    # R/W Main timer
    CL_WEEK = 2
    # R Weekly Schedule
    CL_BOOST_MODE = 3
    # R Boost mode
    CL_FPLC_MODE = 4
    # R/W Fireplace mode
    CL_INT_RH_CTRL = 5
    # R/W Main humidity sensor activation
    CL_EXT_RH_CTRL = 6
    # R/W External humidity sensor activation
    CL_INT_CO2_CTRL = 7
    # R/W Main CO2 sensor activation
    CL_EXT_CO2_CTRL = 8
    # R/W External CO2 sensor activation
    CL_INT_PM2_5_CTRL = 9
    # R/W Main PM2.5 sensor activation
    CL_EXT_PM2_5_CTRL = 10
    # R/W External PM2.5 sensor activation
    CL_INT_VOC_CTRL = 11
    # R/W Main VOC sensor activation
    CL_EXT_VOC_CTRL = 12
    # R/W External VOC sensor activation
    CL_BOOST_SWITCH_CTRL = 13
    # R/W Input activation for the boost mode switch
    CL_FPLC_SWITCH_CTRL = 14
    # R/W Input activation for the fireplace mode switch
    CL_FIRE_ALARM_CTRL = 15
    # R/W Fire alarm sensor activation
    CL_10V_SENSOR_CTRL = 16
    # W Input activation for the external control device 0-10 V
    CL_RESET_FILTER_TIMER = 17
    # W Reset timer countdown to filter replacement
    CL_RESET_ALARM = 18
    # W Reset all alarms
    CL_RESTORE_FACTORY = 19
    # R/W Restore everything to factory settings
    CL_CLOUD_CTRL = 20
    # R/W Activation of control via cloud server
    CL_MIN_SU_AIR_OUT_TEMP_CTRL = 21
    # R/W Minimum room supply air temperature control
    CL_WATER_PRESS_CTRL = 22
    # R/W Heat medium water pressure sensor activation
    CL_WATER_FLOW_CTRL = 23
    # R/W Heat medium water flow sensor activation
    CL_WATER_HEATER_AUTO_RESTART = 24


class DiscreteInputs(Enum):
    # Current input status for the Boost mode switch
    DI_CUR_BOOST_SWITCH = 0
    # Current input status for the Fireplace mode switch
    DI_CUR_FPLC_SWITCH = 1
    # Current status of the fire alarm sensor
    DI_CUR_FIRE_ALARM = 2
    # Humidity setpoint excess indication
    DI_STATUS_RH = 3
    # CO2 setpoint excess indication
    DI_STATUS_CO2 = 4
    # PM2.5 setpoint excess indication
    DI_STATUS_PM2_5 = 5
    # VOC setpoint excess indication
    DI_STATUS_VOC = 6
    # Heater operation indication
    DI_STATUS_HEATER = 7
    # Cooler operation indication
    DI_STATUS_COOLER = 8
    # Electric heater blowdown indication
    DI_STATUS_FAN_BLOWING = 9
    # Current input status for the preheating thermostat
    DI_CUR_PRE_HEATER_THERMOSTAT = 10
    # Current input status for the reheating thermostat
    DI_CUR_MAIN_HEATER_THERMOSTAT = 11
    # Current input status for the differential pressure switch of the supply filter
    DI_CUR_SU_FILTER_PRESS = 12
    # Current input status for the differential pressure switch of the extract filter
    DI_CUR_EX_FILTER_PRESS = 13
    # Current status of the heat medium water pressure sensor
    DI_CUR_WATER_PRESS = 14
    # Current status of the heat medium water flow sensor
    DI_CUR_WATER_FLOW = 15
    # Current input status for the differential pressure switch of the supply fan
    DI_CUR_SU_FAN_PRESS = 16
    # Current input status for the differential pressure switch of the extract fan
    DI_CUR_EX_FAN_PRESS = 17
    # Return water heating indicator before the air handling unit start-up
    DI_WATER_PREHEATING_STATUS = 18
    # Alarm indicator with code No. 0
    DI_ALARM_CODE_0 = 19
    # Alarm indicator with code No. 1
    DI_ALARM_CODE_1 = 20
    # Alarm indicator with code No. 2
    DI_ALARM_CODE_2 = 21
    # Alarm indicator with code No. 3
    DI_ALARM_CODE_3 = 22
    # Alarm indicator with code No. 4
    DI_ALARM_CODE_4 = 23
    # Alarm indicator with code No. 5
    DI_ALARM_CODE_5 = 24
    # Alarm indicator with code No. 6
    DI_ALARM_CODE_6 = 25
    # Alarm indicator with code No. 7
    DI_ALARM_CODE_7 = 26
    # Alarm indicator with code No. 8
    DI_ALARM_CODE_8 = 27
    # Alarm indicator with code No. 9
    DI_ALARM_CODE_9 = 28
    # Alarm indicator with code No. 10
    DI_ALARM_CODE_10 = 29
    # Alarm indicator with code No. 11
    DI_ALARM_CODE_11 = 30
    # Alarm indicator with code No. 12
    DI_ALARM_CODE_12 = 31
    # Alarm indicator with code No. 13
    DI_ALARM_CODE_13 = 32
    # Alarm indicator with code No. 14
    DI_ALARM_CODE_14 = 33
    # Alarm indicator with code No. 15
    DI_ALARM_CODE_15 = 34
    # Alarm indicator with code No. 16
    DI_ALARM_CODE_16 = 35
    # Alarm indicator with code No. 17
    DI_ALARM_CODE_17 = 36
    # Alarm indicator with code No. 18
    DI_ALARM_CODE_18 = 37
    # Alarm indicator with code No. 19
    DI_ALARM_CODE_19 = 38
    # Alarm indicator with code No. 20
    DI_ALARM_CODE_20 = 39
    # Alarm indicator with code No. 21
    DI_ALARM_CODE_21 = 40
    # Alarm indicator with code No. 22
    DI_ALARM_CODE_22 = 41
    # Alarm indicator with code No. 23
    DI_ALARM_CODE_23 = 42
    # Alarm indicator with code No. 24
    DI_ALARM_CODE_24 = 43
    # Alarm indicator with code No. 25
    DI_ALARM_CODE_25 = 44
    # Alarm indicator with code No. 26
    DI_ALARM_CODE_26 = 45
    # Alarm indicator with code No. 27
    DI_ALARM_CODE_27 = 46
    # Alarm indicator with code No. 28
    DI_ALARM_CODE_28 = 47
    # Alarm indicator with code No. 29
    DI_ALARM_CODE_29 = 48
    # Alarm indicator with code No. 30
    DI_ALARM_CODE_30 = 49
    # Alarm indicator with code No. 31
    DI_ALARM_CODE_31 = 50
    # Alarm indicator with code No. 32
    DI_ALARM_CODE_32 = 51
    # Alarm indicator with code No. 33
    DI_ALARM_CODE_33 = 52
    # Alarm indicator with code No. 34
    DI_ALARM_CODE_34 = 53
    # Alarm indicator with code No. 35
    DI_ALARM_CODE_35 = 54
    # Alarm indicator with code No. 36
    DI_ALARM_CODE_36 = 55
    # Alarm indicator with code No. 37
    DI_ALARM_CODE_37 = 56
    # Alarm indicator with code No. 38
    DI_ALARM_CODE_38 = 57
    # Alarm indicator with code No. 39
    DI_ALARM_CODE_39 = 58
    # Alarm indicator with code No. 40
    DI_ALARM_CODE_40 = 59
    # Alarm indicator with code No. 41
    DI_ALARM_CODE_41 = 60
    # Alarm indicator with code No. 42
    DI_ALARM_CODE_42 = 61
    # Alarm indicator with code No. 43
    DI_ALARM_CODE_43 = 62
    # Alarm indicator with code No. 44
    DI_ALARM_CODE_44 = 63
    # Alarm indicator with code No. 45
    DI_ALARM_CODE_45 = 64
    # Alarm indicator with code No. 46
    DI_ALARM_CODE_46 = 65
    # Alarm indicator with code No. 47
    DI_ALARM_CODE_47 = 66
    # Alarm indicator with code No. 48
    DI_ALARM_CODE_48 = 67
    # Alarm indicator with code No. 49
    DI_ALARM_CODE_49 = 68
    # Alarm indicator with code No. 50
    DI_ALARM_CODE_50 = 69
    # Alarm indicator with code No. 51
    DI_ALARM_CODE_51 = 70
    # Alarm indicator with code No. 52
    DI_ALARM_CODE_52 = 71


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


class HoldingRegister(Enum):
    # Ventilation mode:
    # 0 - mode 0 ... 100%, 1 - constant flow, 2 - constant pressure
    HR_VENTILATION_MODE = 0

    # Maximum permissible speed number
    HR_MAXSPEED_MODE = 1

    # Speed number:
    # 1 – Speed 1, 2 – Speed 2, 3 – Speed 3, 4 - Speed 4, 5 - Speed 5, 255 – manual speed setting mode (see HR17)
    HR_SPEED_MODE = 2

    # Minimum possible fan speed
    HR_MINSPEED = 3

    # Maximum possible fan speed
    HR_MAXSPEED = 4

    # Supply fan speed in Standby mode
    HR_SUSPEED0 = 5

    # Extract fan speed in Standby mode
    HR_EXSPEED0 = 6

    # Supply fan speed in Speed 1 mode
    HR_SUSPEED1 = 7

    # Extract fan speed in Speed 1 mode
    HR_EXSPEED1 = 8

    # Supply fan speed in Speed 2 mode
    HR_SUSPEED2 = 9

    # Extract fan speed in Speed 2 mode
    HR_EXSPEED2 = 10

    # Supply fan speed in Speed 3 mode
    HR_SUSPEED3 = 11

    # Extract fan speed in Speed 3 mode
    HR_EXSPEED3 = 12

    # Supply fan speed in Speed 4 mode
    HR_SUSPEED4 = 13

    # Extract fan speed in Speed 4 mode
    HR_EXSPEED4 = 14

    # Supply fan speed in Speed 5 mode
    HR_SUSPEED5 = 15

    # Extract fan speed in Speed 5 mode
    HR_EXSPEED5 = 16

    # Fan speed in manual speed setting mode
    # The balance between supply and exhaust air corresponds to the current preset speeds 1-5
    HR_MANUALSPEED = 17

    # Fan speed while blowing electric heaters
    HR_BLOWINGSPEED = 18

    # Supply fan speed in Boost mode
    HR_BOOST_SUSPEED = 19

    # Extract fan speed in Boost mode
    HR_BOOST_EXSPEED = 20

    # Supply fan speed in Fireplace mode
    HR_FPLC_SUSPEED = 21

    # Extract fan speed in Fireplace mode
    HR_FPLC_EXSPEED = 22

    # Minimum possible air flow of the unit
    HR_MINAIRFLOW = 23

    # Maximum possible air flow of the unit
    HR_MAXAIRFLOW = 24

    # Supply air flow in Standby mode
    HR_SUSPEED0_FLOW = 25

    # Extract air flow in Standby mode
    HR_EXSPEED0_FLOW = 26

    # Supply air flow in Speed 1 mode
    HR_SUSPEED1_FLOW = 27

    # Extract air flow in Speed 1 mode
    HR_EXSPEED1_FLOW = 28

    # Supply air flow in Speed 2 mode
    HR_SUSPEED2_FLOW = 29

    # Extract air flow in Speed 2 mode
    HR_EXSPEED2_FLOW = 30

    # Supply air flow in Speed 3 mode
    HR_SUSPEED3_FLOW = 31

    # Extract air flow in Speed 3 mode
    HR_EXSPEED3_FLOW = 32

    # Supply air flow in Speed 4 mode
    HR_SUSPEED4_FLOW = 33

    # Extract air flow in Speed 4 mode
    HR_EXSPEED4_FLOW = 34

    # Supply air flow in Speed 5 mode
    HR_SUSPEED5_FLOW = 35

    # Extract air flow in Speed 5 mode
    HR_EXSPEED5_FLOW = 36

    # Minimum possible pressure in the air duct
    HR_MINAIRPRESS = 37

    # Maximum possible pressure in the air duct
    HR_MAXAIRPRESS = 38

    # Pressure in the supply air duct in Standby mode
    HR_SUSPEED0_PRESS = 39

    # Pressure in the exhaust air duct in Standby mode
    HR_EXSPEED0_PRESS = 40

    # Pressure in the supply air duct in Speed 1 mode
    HR_SUSPEED1_PRESS = 41

    # Pressure in the exhaust air duct in Speed 1 mode
    HR_EXSPEED1_PRESS = 42

    # Unit operation mode:
    # 0 - ventilation only, 1 - heating, 2 - cooling, 3 - auto
    HR_OPERATION_MODE = 43

    # Room temperature setpoint in normal mode
    HR_SETTEMP = 44

    # Humidity threshold setpoint
    HR_SETRH = 45

    # CO2 threshold setpoint
    HR_SETCO2 = 46

    # PM2.5 threshold setpoint
    HR_SETPM2_5 = 47

    # VOC threshold setpoint
    HR_SETVOC = 48

    # Timer mode:
    # 0 - Standby, 1 - Speed 1, 2 - Speed 2, 3 - Speed 3, 4 - Speed 4, 5 - Speed 5
    HR_TIMER_MODE = 49

    # Room temperature setpoint for the main timer:
    # 0 - ventilation only, +15...+ 30 °C
    HR_SETTIMER_TEMP = 50

    # Time setpoint of the main timer
    HR_SETTIMER_TIME = 51

    # Transition temperature winter/summer
    HR_SETTEMP_WINTERSUMMER = 52

    # Selecting a temperature sensor for controlling room temperature:
    # 0 - in the exhaust air duct, 1 - external sensor in the control panel, 2 - in the supply air duct
    HR_SELTEMP_SENSOR = 53

    # Main heater type:
    # 0 - turn off, 1 - electric, 2 - water
    HR_MAINHEATER_TYPE = 54

    # Cooler control type:
    # 0 - turn off, 1 - discrete, 2 - analogue 0-10 V (integrated)
    HR_COOLER_TYPE = 55

    # Heat exchanger Freeze protection mode:
    # 0 - turn off, 1 - preheating, 2 - bypass/rotor, 3 - fan imbalance
    HR_DEF_MODE = 56

    # Bypass/rotary heat exchanger type:
    # 0 - not available, 1 - bypass with two-point control, 2 - bypass with analogue control,
    # 3 - rotary heat exchanger with discrete control, 4 - rotary heat exchanger with analogue control,
    # 5 - bypass with three-point control
    HR_BPS_ROTOR_TYPE = 57

    # Filter timer setpoint: 0 - turn off the timer, 70...365 days
    HR_SETFILTER_TIMER = 58

    # Setpoint of the Boost mode turn-off delay
    HR_BOOSTDELAYSWITCHINGOFF = 59

    # Setpoint of the Boost mode turn-on delay
    HR_BOOSTDELAYSWITCHINGON = 60

    # RTC time
    HR_RTC_TIME = 61

    # RTC calendar
    HR_RTC_CALENDAR = 63

    # Maximum value of the main CO2 sensor
    HR_MAXCO2_INT = 65

    # Maximum value of the main PM2.5 sensor
    HR_MAXPM2_5_INT = 66

    # Minimum room supply air temperature control setpoint
    HR_SETMINSUAIR_OUTTEMP = 67

    # Main heater operation mode:
    # 1 - control 0 - 100 %, 2 - AUTO
    HR_MAINHEATERMODE = 68

    # Manual control of the main heater
    HR_SETMAINHEATERMANUAL = 69

    # Cooler operation mode:
    # 1 - turn on the cooler with discrete configuration, control 0-100 % with analogue configuration,
    # 2 - AUTO
    HR_COOLERMODE = 70

    # Manual cooler control with analogue configuration
    HR_SETCOOLERMANUAL = 71

    # Preheating operation mode:
    # 1 - control 0 - 100 %, 2 - AUTO
    HR_PREHEATERMODE = 72

    # Manual preheating control
    HR_SETPREHEATERMANUAL = 73

    # Bypass/rotary heat exchanger operation mode:
    # 0 - close the bypass/start the rotor,
    # 1 - open the bypass/stop the rotor with discrete configuration, control 0-100 % with analogue configuration,
    # 2 - AUTO
    HR_BPS_ROTOR_MODE = 74

    # Manual bypass/rotor control with analogue configuration:
    # 0 % - bypass closed/rotor rotates at maximum speed, 100 %/bypass open, rotor stopped
    HR_SETBPSROTOR_MANUAL = 75

    # Kp coefficient of the PID humidity controller
    HR_RH_KP = 76

    # Ki coefficient of the PID humidity controller
    HR_RH_KI = 77

    # Kd coefficient of the PID humidity controller
    HR_RH_KD = 78

    # Kp coefficient of the PID CO2 level controller
    HR_CO2_KP = 79

    # Ki coefficient of the PID CO2 level controller
    HR_CO2_KI = 80

    # Kd coefficient of the PID CO2 level controller
    HR_CO2_KD = 81

    # Kp coefficient of the PID PM2.5 level controller
    HR_PM2_5_KP = 82

    # Ki coefficient of the PID PM2.5 level controller
    HR_PM2_5_KI = 83

    # Kd coefficient of the PID PM2.5 level controller
    HR_PM2_5_KD = 84

    # Kp coefficient of the PID VOC level controller
    HR_VOC_KP = 85

    # Ki coefficient of the PID VOC level controller
    HR_VOC_KI = 86

    # Kd coefficient of the PID VOC level controller
    HR_VOC_KD = 87

    # Kp coefficient of the PID preheating controller
    HR_PREHEATER_KP = 88

    # Ki coefficient of the PID preheating controller
    HR_PREHEATER_KI = 89

    # Kd coefficient of the PID preheating controller
    HR_PREHEATER_KD = 90

    # Kp coefficient of the PID reheating controller
    HR_MAINHEATER_KP = 91

    # Ki coefficient of the PID reheating controller
    HR_MAINHEATER_KI = 92

    # Kd coefficient of the PID reheating controller
    HR_MAINHEATER_KD = 93

    # Kp coefficient of the PID bypass/rotary heat exchanger controller
    HR_BPS_ROTOR_KP = 94

    # Ki coefficient of the PID bypass/rotary heat exchanger controller
    HR_BPS_ROTOR_KI = 95

    # Kd coefficient of the PID bypass/rotary heat exchanger controller
    HR_BPS_ROTOR_KD = 96

    # Kp coefficient of the PID condenser unit controller
    HR_KKB_KP = 97

    # Ki coefficient of the PID condenser unit controller
    HR_KKB_KI = 98

    # Kd coefficient of the PID condenser unit controller
    HR_KKB_KD = 99

    # Kp coefficient of the PID return heat medium controller
    HR_RETURNWATER_KP = 100

    # Ki coefficient of the PID return heat medium controller
    HR_RETURNWATER_KI = 101

    # Kd coefficient of the PID return heat medium controller
    HR_RETURNWATER_KD = 102

    # Fan alarm control type
    HR_FAN_ALARM_CTRL = 103

    # Time for fan alarm detection
    HR_SETTIMEDETECTFANALARM = 104

    # Damper opening time (fan turn-on delay)
    HR_SETTIMEOPENVALVE = 105

    # Electric heater blowdown time
    HR_SETTIMEFANBLOWING = 106

    # Minimum downtime of the condenser unit before restarting
    HR_KKB_MINTIMEOFF = 107

    # Minimum operating time of the condenser unit before shutdown
    HR_KKB_MINTIMEON = 108

    # Hysteresis for turning the condenser unit on/off with discrete control
    HR_KKB_HYSTERESIS = 109

    # Bypass location
    HR_BPS_POSITION = 110

    # Opening time of the bypass with three-point control
    HR_TIMEOPENBPS = 111

    # Correction of the intake air temperature sensor at the unit inlet
    HR_CORRTEMP_SUAIRIN = 112

    # Correction of the supply air temperature sensor at the unit outlet
    HR_CORRTEMP_SUAIR_OUT = 113

    # Correction of the extract air temperature sensor at the unit inlet
    HR_CORRTEMP_EXAIRIN = 114

    # Correction of the exhaust air temperature sensor at the unit outlet
    HR_CORRTEMP_EXAIR_OUT = 115

    # Correction of the return heat medium temperature sensor
    HR_CORRTEMP_WATER = 116

    # Correction of the outdoor air temperature sensor
    HR_CORRTEMP_EXT = 117

    # Minimum position of the water heater valve in winter
    HR_WATERVALVEMINPOS = 118

    # TIME FOR DETECTING RETURN HEAT MEDIUM UNDER-HEATING ALARM BEFORE THE AHU START IN WINTER
    HR_WATER_MAX_START_TIME = 119

    # INITIAL VALUE OF THE RETURN HEAT MEDIUM TEMPERATURE REQUIRED FOR THE AHU START IN WINTER
    # AT OUTDOOR TEMPERATURE >= +10 °C
    HR_WATER_MIN_START_TEMP = 120

    # FINAL VALUE OF THE RETURN HEAT MEDIUM TEMPERATURE REQUIRED FOR THE AHU START IN WINTER
    # AT OUTDOOR TEMPERATURE <= -30 °C
    HR_WATER_MAX_START_TEMP = 121

    # INITIAL VALUE OF THE RETURN HEAT MEDIUM TEMPERATURE FOR THE AHU SHUTDOWN CAUSED BY A
    # FREEZE ALARM IN WINTER AT OUTDOOR TEMPERATURE >= +10 °C
    HR_WATER_MIN_ALARM_TEMP = 122

    # FINAL VALUE OF THE RETURN HEAT MEDIUM TEMPERATURE FOR THE AHU SHUTDOWN CAUSED BY A FREEZE
    # ALARM IN WINTER AT OUTDOOR TEMPERATURE <= -30 °C
    HR_WATER_MAX_ALARM_TEMP = 123

    # PASSWORD TO ENTER THE ENGINEERING MENU. THE STRING SHOULD BE 1-4 CHARACTERS LONG.
    # THE END OF THE STRING IS DETERMINED BY THE NULL CHARACTER
    HR_ENGINEER_PWD = 124

    # SPEED NUMBER FOR MO. IN THE 1ST TIME PERIOD
    HR_SETWEEK_MO_1ST_PERIOD_SPEED_TEMP = 126

    # HOURS OF THE END OF THE 1ST PERIOD ON MO.
    HR_SETWEEK_MO_1ST_PERIOD_END_HOURS_MINUTES = 127

    # SPEED NUMBER FOR MO. IN THE 2ND TIME PERIOD
    HR_SETWEEK_MO_2ND_PERIOD_SPEED = 128

    # TEMPERATURE SETPOINT FOR MO. IN THE 2ND PERIOD
    HR_SETWEEK_MO_2ND_PERIOD_TEMP = 128

    # HOURS OF THE END OF THE 2ND PERIOD ON MO.
    HR_SETWEEK_MO_2ND_PERIOD_END_HOURS = 129

    # MINUTES OF THE END OF THE 2ND PERIOD ON MO.
    HR_SETWEEK_MO_2ND_PERIOD_END_MINUTES = 129

    # SPEED NUMBER FOR MO. IN THE 3RD TIME PERIOD
    HR_SETWEEK_MO_3RD_PERIOD_SPEED = 130

    # TEMPERATURE SETPOINT FOR MO. IN THE 3RD PERIOD
    HR_SETWEEK_MO_3RD_PERIOD_TEMP = 130

    # HOURS OF THE END OF THE 3RD PERIOD ON MO.
    HR_SETWEEK_MO_3RD_PERIOD_END_HOURS = 131

    # MINUTES OF THE END OF THE 3RD PERIOD ON MO.
    HR_SETWEEK_MO_3RD_PERIOD_END_MINUTES = 131

    # SPEED NUMBER FOR MO. IN THE 4TH TIME PERIOD
    HR_SETWEEK_MO_4TH_PERIOD_SPEED = 132

    # TEMPERATURE SETPOINT FOR MO. IN THE 4TH PERIOD
    HR_SETWEEK_MO_4TH_PERIOD_TEMP = 132

    # RESERVED. THE END OF THE 4TH PERIOD IS ALWAYS AT 23:59
    HR_SETWEEK_MO_4TH_PERIOD_END = 133

    # SPEED NUMBER FOR TU. IN THE 1ST TIME PERIOD
    HR_SETWEEK_TU_1ST_PERIOD_SPEED = 134

    # TEMPERATURE SETPOINT FOR TU. IN THE 1ST PERIOD
    HR_SETWEEK_TU_1ST_PERIOD_TEMP = 134

    # HOURS OF THE END OF THE 1ST PERIOD ON TU.
    HR_SETWEEK_TU_1ST_PERIOD_END_HOURS = 135

    # MINUTES OF THE END OF THE 1ST PERIOD ON TU.
    HR_SETWEEK_TU_1ST_PERIOD_END_MINUTES = 135

    # SPEED NUMBER FOR TU. IN THE 2ND TIME PERIOD
    HR_SETWEEK_TU_2ND_PERIOD_SPEED = 136

    # TEMPERATURE SETPOINT FOR TU. IN THE 2ND PERIOD
    HR_SETWEEK_TU_2ND_PERIOD_TEMP = 136

    # HOURS OF THE END OF THE 2ND PERIOD ON TU.
    HR_SETWEEK_TU_2ND_PERIOD_END_HOURS = 137

    # MINUTES OF THE END OF THE 2ND PERIOD ON TU.
    HR_SETWEEK_TU_2ND_PERIOD_END_MINUTES = 137

    # SPEED NUMBER FOR TU. IN THE 3RD TIME PERIOD
    HR_SETWEEK_TU_3RD_PERIOD_SPEED = 138

    # TEMPERATURE SETPOINT FOR TU. IN THE 3RD PERIOD
    HR_SETWEEK_TU_3RD_PERIOD_TEMP = 138

    # HOURS OF THE END OF THE 3RD PERIOD ON TU.
    HR_SETWEEK_TU_3RD_PERIOD_END_HOURS = 139

    # MINUTES OF THE END OF THE 3RD PERIOD ON TU.
    HR_SETWEEK_TU_3RD_PERIOD_END_MINUTES = 139

    # SPEED NUMBER FOR TU. IN THE 4TH TIME PERIOD
    HR_SETWEEK_TU_4TH_PERIOD_SPEED = 140

    # TEMPERATURE SETPOINT FOR TU. IN THE 4TH PERIOD
    HR_SETWEEK_TU_4TH_PERIOD_TEMP = 140

    # RESERVED. THE END OF THE 4TH PERIOD IS ALWAYS AT 23:59
    HR_SETWEEK_TU_4TH_PERIOD_END = 141

    # SPEED NUMBER FOR WE. IN THE 1ST TIME PERIOD
    HR_SETWEEK_WE_1ST_PERIOD_SPEED = 142

    # TEMPERATURE SETPOINT FOR WE. IN THE 1ST PERIOD
    HR_SETWEEK_WE_1ST_PERIOD_TEMP = 142

    # HOURS OF THE END OF THE 1ST PERIOD ON WE.
    HR_SETWEEK_WE_1ST_PERIOD_END_HOURS = 143

    # MINUTES OF THE END OF THE 1ST PERIOD ON WE.
    HR_SETWEEK_WE_1ST_PERIOD_END_MINUTES = 143

    # SPEED NUMBER FOR WE. IN THE 2ND TIME PERIOD
    HR_SETWEEK_WE_2ND_PERIOD_SPEED = 144

    # TEMPERATURE SETPOINT FOR WE. IN THE 2ND PERIOD
    HR_SETWEEK_WE_2ND_PERIOD_TEMP = 144

    # HOURS OF THE END OF THE 2ND PERIOD ON WE.
    HR_SETWEEK_WE_2ND_PERIOD_END_HOURS = 145

    # MINUTES OF THE END OF THE 2ND PERIOD ON WE.
    HR_SETWEEK_WE_2ND_PERIOD_END_MINUTES = 145

    # SPEED NUMBER FOR WE. IN THE 3RD TIME PERIOD
    HR_SETWEEK_WE_3RD_PERIOD_SPEED = 146

    # TEMPERATURE SETPOINT FOR WE. IN THE 3RD PERIOD
    HR_SETWEEK_WE_3RD_PERIOD_TEMP = 146

    # HOURS OF THE END OF THE 3RD PERIOD ON WE.
    HR_SETWEEK_WE_3RD_PERIOD_END_HOURS = 147

    # MINUTES OF THE END OF THE 3RD PERIOD ON WE.
    HR_SETWEEK_WE_3RD_PERIOD_END_MINUTES = 147

    # SPEED NUMBER FOR WE. IN THE 4TH TIME PERIOD
    HR_SETWEEK_WE_4TH_PERIOD_SPEED = 148

    # TEMPERATURE SETPOINT FOR WE. IN THE 4TH PERIOD
    HR_SETWEEK_WE_4TH_PERIOD_TEMP = 148

    # RESERVED. THE END OF THE 4TH PERIOD IS ALWAYS AT 23:59
    HR_SETWEEK_WE_4TH_PERIOD_END = 149

    # 150 R/W
    # Speed number for Th. in the 1st time period
    # Temperature setpoint for Th. in the 1st period
    HR_SETWEEK_TH_1 = 150

    # 151 R/W
    # Hours of the end of the 1st period on Th.
    # Minutes of the end of the 1st period on Th.
    HR_ENDPERIOD1_TH = 151

    # 152 R/W
    # Speed number for Th. in the 2nd time period
    # Temperature setpoint for Th. in the 2nd period
    HR_SETWEEK_TH_2 = 152

    # 153 R/W
    # Hours of the end of the 2nd period on Th.
    # Minutes of the end of the 2nd period on Th.
    HR_ENDPERIOD2_TH = 153

    # 154 R/W
    # Speed number for Th. in the 3rd time period
    # Temperature setpoint for Th. in the 3rd period
    HR_SETWEEK_TH_3 = 154

    # 155 R/W
    # Hours of the end of the 3rd period on Th.
    # Minutes of the end of the 3rd period on Th.
    HR_ENDPERIOD3_TH = 155

    # 156 R/W
    # Speed number for Th. in the 4th time period
    # Temperature setpoint for Th. in the 4th period
    HR_SETWEEK_TH_4 = 156

    # 157 R
    # Reserved. The end of the 4th period is always at 23:59
    HR_RESERVED_TH = 157

    # 158 R/W
    # Speed number for Fr. in the 1st time period
    # Temperature setpoint for Fr. in the 1st period
    HR_SETWEEK_FR_1 = 158

    # 159 R/W
    # Hours of the end of the 1st period on Fr.
    # Minutes of the end of the 1st period on Fr.
    HR_ENDPERIOD1_FR = 159

    # 160 R/W
    # Speed number for Fr. in the 2nd time period
    # Temperature setpoint for Fr. in the 2nd period
    HR_SETWEEK_FR_2 = 160

    # 161 R/W
    # Hours of the end of the 2nd period on Fr.
    # Minutes of the end of the 2nd period on Fr.
    HR_ENDPERIOD2_FR = 161

    # 162 R/W
    # Speed number for Fr. in the 3rd time period
    # Temperature setpoint for Fr. in the 3rd period
    HR_SETWEEK_FR_3 = 162

    # 163 R/W
    # Hours of the end of the 3rd period on Fr.
    # Minutes of the end of the 3rd period on Fr.
    HR_ENDPERIOD3_FR = 163

    # 164 R/W
    # Speed number for Fr. in the 4th time period
    # Temperature setpoint for Fr. in the 4th period
    HR_SETWEEK_FR_4 = 164

    # 165 R
    # Reserved. The end of the 4th period is always at 23:59
    HR_RESERVED_FR = 165

    # 166 R/W
    # Speed number for Sa. in the 1st time period
    # Temperature setpoint for Sa. in the 1st period
    HR_SETWEEK_SA_1 = 166

    # 167 R/W
    # Hours of the end of the 1st period on Sa.
    # Minutes of the end of the 1st period on Sa.
    HR_ENDPERIOD1_SA = 167

    # 168 R/W
    # Speed number for Sa. in the 2nd time period
    # Temperature setpoint for Sa. in the 2nd period
    HR_SETWEEK_SA_2 = 168

    # 169 R/W
    # Hours of the end of the 2nd period on Sa.
    # Minutes of the end of the 2nd period on Sa.
    HR_ENDPERIOD2_SA = 169

    # 170 R/W
    # Speed number for Sa. in the 3rd time period
    # Temperature setpoint for Sa. in the 3rd period
    HR_SETWEEK_SA_3 = 170

    # 171 R/W
    # Hours of the end of the 3rd period on Sa.
    # Minutes of the end of the 3rd period on Sa.
    HR_ENDPERIOD3_SA = 171

    # 172 R/W
    # Speed number for Sa. in the 4th time period
    # Temperature setpoint for Sa. in the 4th period
    HR_SETWEEK_SA_4 = 172

    # 173 R
    # Reserved. The end of the 4th period is always at 23:59
    HR_RESERVED_SA = 173

    # 174 R/W
    # Speed number for Su. in the 1st time period
    # Temperature setpoint for Su. in the 1st period
    HR_SETWEEK_SU_1 = 174

    # 175 R/W
    # Hours of the end of the 1st period on Su.
    # Minutes of the end of the 1st period on Su.
    HR_ENDPERIOD1_SU = 175

    # 176 R/W
    # Speed number for Su. in the 2nd time period
    # Temperature setpoint for Su. in the 2nd period
    HR_SETWEEK_SU_2 = 176

    # 177 R/W
    # Hours of the end of the 2nd period on Su.
    # Minutes of the end of the 2nd period on Su.
    HR_ENDPERIOD2_SU = 177

    # 178 R/W
    # Speed number for Su. in the 3rd time period
    # Temperature setpoint for Su. in the 3rd period
    HR_SETWEEK_SU_3 = 178

    # 179 R/W
    # Hours of the end of the 3rd period on Su.
    # Minutes of the end of the 3rd period on Su.
    HR_ENDPERIOD3_SU = 179

    # 180 R/W
    # Speed number for Su. in the 4th time period
    # Temperature setpoint for Su. in the 4th period
    HR_SETWEEK_SU_4 = 180

    # 181 R
    # Reserved. The end of the 4th period is always at 23:59
    HR_RESERVED_SU = 181
