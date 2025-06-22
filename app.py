from flask import Flask, send_from_directory, request, jsonify, send_file
import json
import serial
import os
from datetime import datetime

# ========== SERIAL CONFIGURATION ==========
SERIAL_PORT = "COM9"
SERIAL_BAUD = 9600
serial_conn = None

print(f"[INFO] Using serial port: {SERIAL_PORT} @ {SERIAL_BAUD} baud")

# ========== FLASK SETUP ==========
app = Flask(__name__, static_folder=".")
HISTORY_FILE = "history.json"

# Initialize history file if it doesn't exist
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)


def get_serial_connection():
    global serial_conn
    if serial_conn is not None:
        return serial_conn
    try:
        serial_conn = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=1)
        print(f"[OK] Serial connection established on {SERIAL_PORT}")
    except Exception as e:
        print(f"[ERROR] Could not open serial port {SERIAL_PORT}: {e}")
        serial_conn = None
    return serial_conn


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/serial_event', methods=['POST'])
def serial_event():
    data = request.get_json(force=True, silent=True)
    if not isinstance(data, dict):
        return jsonify({'status': 'error', 'message': 'Invalid JSON'}), 400

    ser = get_serial_connection()

    # Save to history.json
    entry = {
        "plate": data.get("plate", "UNKNOWN"),
        "action": "Entered" if data.get("action") == 1 else "Left",
        "slots": data.get("slots"),
        "used": data.get("used"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(HISTORY_FILE, "r+") as f:
            history_data = json.load(f)
            history_data.append(entry)
            f.seek(0)
            f.truncate()
            json.dump(history_data, f, indent=4)
    except Exception as e:
        print(f"[ERROR] Failed to save history: {e}")

    if ser:
        try:
            json_data = json.dumps(data) + '\n'
            ser.write(json_data.encode('utf-8'))
            print(f"[→] Sent to serial: {json_data.strip()}")
        except Exception as e:
            print(f"[ERROR] Failed to write to serial: {e}")
            return jsonify({'status': 'error', 'message': 'Serial write failed'}), 500
    else:
        print("[✘] No serial connection. Fallback to console.")
        print("Serial output:", json.dumps(data))

    return jsonify({'status': 'ok'})


@app.route('/download_history')
def download_history():
    if not os.path.exists(HISTORY_FILE):
        return jsonify({"error": "No history found"}), 404
    return send_file(HISTORY_FILE, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
