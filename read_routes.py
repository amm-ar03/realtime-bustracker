import json

def read_json(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data



