from flask import Flask, render_template, jsonify
from pymodbus.client import ModbusTcpClient

app = Flask(__name__)
client = ModbusTcpClient("localhost", port=502)

@app.route("/")
def simulation():
    # Fetch initial data from Modbus
    temp = client.read_holding_registers(0, 1).registers[0]
    pressure = client.read_holding_registers(1, 1).registers[0]
    motor_state = client.read_coils(0, 1).bits[0]
    return render_template("simulation.html", temperature=temp, pressure=pressure, motor_state=motor_state)

@app.route("/live_data", methods=["GET"])
def live_data():
    # Fetch live data from Modbus
    temp = client.read_holding_registers(0, 1).registers[0]
    pressure = client.read_holding_registers(1, 1).registers[0]
    motor_state = client.read_coils(0, 1).bits[0]
    return jsonify({"temperature": temp, "pressure": pressure, "motor_state": motor_state})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

