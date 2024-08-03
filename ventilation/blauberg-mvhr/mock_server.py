from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import StartTcpServer
from coil_register import CoilRegister


def run_server():
    # Create data block with initial values based on the provided documentation
    coils = [0] * (max(coil.value for coil in CoilRegister) + 1)
    coils[CoilRegister.CL_BoostSWITCH_CTRL.value] = 1
    coils[CoilRegister.CL_FplcSWITCH_CTRL.value] = 1
    coils[CoilRegister.CL_RESET_FILTER_TIMER.value] = 1
    coils[CoilRegister.CL_RESET_ALARM.value] = 1
    coils[CoilRegister.CL_RESTORE_FACTORY.value] = 1
    coils[CoilRegister.CL_MinSuAirOutTEMP_CTRL.value] = 1
    coils[CoilRegister.CL_WaterPRESS_CTRL.value] = 1
    coils[CoilRegister.CL_WaterHeaterAutoRestart.value] = 1

    store = ModbusSlaveContext(
        co=ModbusSequentialDataBlock(0, coils),
        di=ModbusSequentialDataBlock(0, [0]*100),  # Discrete Inputs (1 bit registers)
        hr=ModbusSequentialDataBlock(0, [0]*100),  # Holding Registers (16 bit registers)
        ir=ModbusSequentialDataBlock(0, [0]*100)   # Input Registers (16 bit registers)
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