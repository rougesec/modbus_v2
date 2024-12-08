from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore.store import ModbusSequentialDataBlock
import random
import threading
import time

# Create Modbus data blocks
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [0] * 10),  # Discrete Inputs (e.g., switches)
    co=ModbusSequentialDataBlock(0, [0] * 10),  # Coils (e.g., actuators)
    hr=ModbusSequentialDataBlock(0, [25, 50, 75]),  # Holding Registers (e.g., sensors)
    ir=ModbusSequentialDataBlock(0, [0] * 10)   # Input Registers
)
context = ModbusServerContext(slaves=store, single=True)

def update_sensors():
    """
    Simulates sensor updates periodically by modifying holding registers (HR).
    """
    while True:
        # Generate random sensor values
        temp = random.randint(20, 100)  # Simulated temperature
        pressure = random.randint(50, 150)  # Simulated pressure
        valve_state = context[0x00].getValues(1, 0, 1)[0]  # Read actuator state (Coil)

        # Update holding registers (HR) with new sensor values
        context[0x00].setValues(3, 0, [temp])       # Update temperature
        context[0x00].setValues(3, 1, [pressure])   # Update pressure

        print(f"Updated Sensor Values - Temperature: {temp}, Pressure: {pressure}, Valve State: {valve_state}")
        time.sleep(5)

# Start Modbus server
if __name__ == "__main__":
    # Start the sensor update thread
    threading.Thread(target=update_sensors, daemon=True).start()

    # Start the Modbus server with the context and address
    StartTcpServer(context=context, address=("0.0.0.0", 502))

