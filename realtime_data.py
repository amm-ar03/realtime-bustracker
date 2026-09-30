import requests
import os
import time
import json
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToJson

REALTIME_DATA_URL = 'https://bct.tmix.se/gtfs-realtime/vehicleupdates.pb?operatorIds=48'
TRIP_UPDATES_URL = 'https://bct.tmix.se/gtfs-realtime/tripupdates.pb?operatorIds=48'

def download_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Successfully downloaded")
            return response.content
        else:
            print(f"Failed to fetch data. Status code : {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"error fetching data: {e}")
        return None

def proto_to_json(data):
    try:
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(data)
        json_data =  MessageToJson(feed)
        print("Protobuf data converted to JSON")
        return json_data
    except Exception as e:
        print(f"Error converting protobuf data to JSON: {e}")
        return None
    
def save_data(data, filename):
    tmp = filename + '.tmp'
    try:
        with open(tmp, 'w') as f:
            f.write(data)
        os.replace(tmp, filename)
        print(f"Saved GTFS Realtime data to {filename}")
    except Exception as e:
        print(f"Error saving data {e}")

def poll_and_save(url=REALTIME_DATA_URL, filename='gtfs_realtime.json', interval=5):
    while True:
        data = download_data(url)
        if data:
            json_data = proto_to_json(data)
            if json_data:
                save_data(json_data, filename)
        time.sleep(interval)
        
def poll_trip_updates(url=TRIP_UPDATES_URL, filename='gtfs_trip_updates.json', interval=10):
    while True:
        data = download_data(url)
        if data:
            json_data = proto_to_json(data)
            if json_data:
                save_data(json_data, filename)
        time.sleep(interval)

if __name__ == "__main__":
    """
    while True:
        data = download_data(REALTIME_DATA_URL)
        
        if data:
            json_data = proto_to_json(data)
            if json_data:
                save_data(json_data, 'gtfs_realtime.json')
        time.sleep(5)
    """
    poll_and_save()