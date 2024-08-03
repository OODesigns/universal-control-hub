from enum import Enum

class CoilRegister(Enum):
    CL_POWER = 0  # R/W Coils (1-bit registers) - modbus functions: 1, 5, 15
    CL_TIMER = 1  # R/W Unit On/Off
    CL_WEEK = 2  # R/W Main timer
    CL_Boost_MODE = 3  # R Weekly Schedule
    CL_FPLC_MODE = 4  # R Boost mode
    CL_IntRH_CTRL = 5  # R/W Fireplace mode
    CL_ExtRH_CTRL = 6  # R/W Main humidity sensor activation
    CL_IntCO2_CTRL = 7  # R/W External humidity sensor activation
    CL_ExtCO2_CTRL = 8  # R/W Main CO2 sensor activation
    CL_IntPM2_5_CTRL = 9  # R/W External CO2 sensor activation
    CL_ExtPM2_5_CTRL = 10  # R/W Main PM2.5 sensor activation
    CL_IntVOC_CTRL = 11  # R/W External PM2.5 sensor activation
    CL_ExtVOC_CTRL = 12  # R/W Main VOC sensor activation
    CL_BoostSWITCH_CTRL = 13  # R/W External VOC sensor activation
    CL_FplcSWITCH_CTRL = 14  # R/W Input activation for the boost mode switch
    CL_FireALARM_CTRL = 15  # R/W Input activation for the fireplace mode switch
    CL_10V_SENSOR_CTRL = 16  # R/W Fire alarm sensor activation
    CL_RESET_FILTER_TIMER = 17  # W Input activation for the external control device 0-10 V
    CL_RESET_ALARM = 18  # W Reset timer countdown to filter replacement
    CL_RESTORE_FACTORY = 19  # W Reset all alarms
    CL_CLOUD_CTRL = 20  # R/W Restore everything to factory settings
    CL_MinSuAirOutTEMP_CTRL = 21  # R/W Activation of control via cloud server
    CL_WaterPRESS_CTRL = 22  # R/W Minimum room supply air temperature control
    CL_WaterFLOW_CTRL = 23  # R/W Heat medium water pressure sensor activation
    CL_WaterHeaterAutoRestart = 24  # R/W Heat medium water flow sensor activation