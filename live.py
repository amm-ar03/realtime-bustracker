import logging
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import time
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
@app.route('/')
def index():
    return render_template('index.html')

def emit_data():
    while True:
        try:
            with open('gtfs_realtime.json', 'r') as json_file:
                feed_dict = json.load(json_file)

                socketio.emit('vehicle-update', feed_dict)
                # Add vehicle positions to the map
                for entity in feed_dict['entity']:
                    if 'vehicle' in entity:
                        vehicle = entity['vehicle']
                        position = vehicle.get('position', {})
                        latitude = position.get('latitude')
                        longitude = position.get('longitude')
                        if latitude and longitude:
                            route_id = vehicle.get('trip', {}).get('routeId', 'N/A')
                            vehicle_status = vehicle.get('currentStatus', 'UNKNOWN')
                            socketio.emit('vehicle_update', {'latitude' : latitude, 'longitude' : longitude,
                                                'route_id': route_id})
            time.sleep(30)

        except Exception as e:
            print(f"Error updating map: {e}")

@socketio.on('connect')
def connect():
    print("connected")


if __name__ == "__main__":
    data_thread = Thread(target=emit_data)
    data_thread.daemon = True
    data_thread.start()
    socketio.run(app, host='0.0.0.0', port=3030)

