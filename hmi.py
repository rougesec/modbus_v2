from flask import Flask, render_template, request, jsonify
from pymodbus.client import ModbusTcpClient

app = Flask(__name__)

# Modbus client connection setup
client = ModbusTcpClient("localhost", port=502)

# Route for the main HMI dashboard
@app.route("/")
def hmi():
    try:
        # Read the temperature, pressure, and motor state
        temp = client.read_holding_registers(0, 1).registers[0]
        pressure = client.read_holding_registers(1, 1).registers[0]
        motor_state = client.read_coils(0, 1).bits[0]
        
        # Return the rendered template with sensor data
        return render_template("hmi.html", temperature=temp, pressure=pressure, motor_state=motor_state)
    except Exception as e:
        return f"Error reading Modbus data: {e}"

# Route to toggle the motor state (ON/OFF)
@app.route("/toggle_motor", methods=["POST"])
def toggle_motor():
    try:
        # Read current motor state
        motor_state = client.read_coils(0, 1).bits[0]
        
        # Toggle the motor state
        client.write_coil(0, not motor_state)
        
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Route to fetch live data for temperature, pressure, and motor state in JSON format
@app.route("/live_data", methods=["GET"])
def live_data():
    try:
        # Fetch current live data
        temp = client.read_holding_registers(0, 1).registers[0]
        pressure = client.read_holding_registers(1, 1).registers[0]
        motor_state = client.read_coils(0, 1).bits[0]
        
        # Return live data in JSON format
        return jsonify({"temperature": temp, "pressure": pressure, "motor_state": motor_state})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

