from flask import Flask, render_template
from flask_socketio import SocketIO
from sensors_logic import LogicHandler
from threading import Thread, Event
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

logic_handler = LogicHandler()
stop_event = Event()

@app.route('/')
def index():
    return render_template('dashboard.html')

def sensor_data_thread():
    print("Starting sensor data thread") # TODO: Delete
    logic_handler.connect_to_sensors()
    try:
        while not stop_event.is_set():
            external_xyz, internal_xyz = logic_handler.read_xyz_data()
            external_mag = logic_handler.calculate_magnitude(external_xyz)
            internal_mag = logic_handler.calculate_magnitude(internal_xyz)

            data = {
                "external": {
                    "x": external_xyz[0],
                    "y": external_xyz[1],
                    "z": external_xyz[2],
                    "magnitude": external_mag
                },
                "internal": {
                    "x": internal_xyz[0],
                    "y": internal_xyz[1],
                    "z": internal_xyz[2],
                    "magnitude": internal_mag
                }
            }
            # print(external_xyz) # TODO: Delete

            socketio.emit('sensor_data', {'x': external_xyz[0], 'y': external_xyz[1], 'z': external_xyz[2]})
            time.sleep(0.1)
    except KeyboardInterrupt:
        logic_handler.close_sensors()

@socketio.on('connect')
def handle_connect():
    print("Client connected.")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected.")

if __name__ == "__main__":
    print("Starting main program")
    thread = threading.Thread(target=sensor_data_thread)
    thread.daemon = True
    thread.start()
    try:
        socketio.run(app, host='127.0.0.1', port=5050)
    finally:
        stop_event.set()
        thread.join()
        logic_handler.close_sensors

