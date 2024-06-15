import gtfs_realtime_pb2
import json
from google.protobuf.json_format import MessageToJson

def proto_to_txt(proto):
    return json.loads(MessageToJson(proto))

file_path = '/Users/ammar/Desktop/transit/vehicle_updates.pb'

with open(file_path, 'rb') as f:
    data = f.read()

feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(data)

feed_dict = proto_to_txt(feed)

with open('gtfs_realtime.json', 'w') as json_file:
    json.dump(feed_dict, json_file, indent=4)

print("data saved to json")