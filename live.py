import logging
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import time
import socket
import os 
from threading import Thread

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

with open('routes.json', 'r') as json_file:
    routes_data = json.load(json_file)
    routes_dict = {route['route_id']: route['headsign'] for route in routes_data}

@app.route('/')
def index():
    return render_template('index.html')

def emit_data():
    while True:
        try:
            try:
                with open('gtfs_realtime.json', 'r') as f:
                    feed_dict = json.load(f)
            except json.JSONDecodeError:
                time.sleep(0.2)
                continue

            entities = feed_dict.get('entity', [])

            sent = 0
            example = None
            for e in entities:
                v = e.get('vehicle')
                if not v: 
                    continue
                pos = v.get('position', {})
                lat, lon = pos.get('latitude'), pos.get('longitude')
                if lat is None or lon is None:
                    continue

                trip = v.get('trip', {})
                payload = {
                    'latitude': lat,
                    'longitude': lon,
                    'trip_id': trip.get('tripId', 'UNKNOWN'),
                    'route_id': trip.get('routeId', 'N/A'),
                    'direction_id': trip.get('directionId'),
                    'vehicle_id': v.get('vehicle', {}).get('id', 'UNKNOWN'),
                    'vehicle_status': v.get('currentStatus', 'UNKNOWN'),
                    'vehicle_seats': v.get('occupancyStatus', 'UNKNOWN'),
                    'vehicle_speed': pos.get('speed'),
                }
                socketio.emit('vehicle_update', payload)
                sent += 1
                if example is None:
                    example = payload  # keep first one

            time.sleep(5)
        except Exception as e:
            print("emit_data error:", e)
            time.sleep(1)
            




@socketio.on('connect')
def connect():
    print("connected")
    
if __name__ == "__main__":
    host = '0.0.0.0'
    port = 3031
    print(f"Local: http://localhost:{port}")
    #data_thread = Thread(target=emit_data)
    #data_thread.daemon = True
    #data_thread.start()
    t = Thread(target=emit_data, daemon=True)
    t.start()
    
    socketio.run(app, host=host, port=port, debug=True, use_reloader=False)

