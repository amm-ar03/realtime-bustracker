import csv
import json

headsign_map = {}

with open("trips.txt", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        headsign = row["trip_headsign"].strip()
        direction_id = int(row["direction_id"])

        if headsign not in headsign_map:
            headsign_map[headsign] = direction_id

print("const headsignDirectionMap = {")
for headsign, direction_id in headsign_map.items():
    print(f'  {json.dumps(headsign)}: {direction_id},')
print("};")
