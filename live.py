import json
import folium
from datetime import datetime
import os
import time

def update_map(filename):
    while True:
        try:
            with open(filename, 'r') as json_file:
                feed_dict = json.load(json_file)

            m = folium.Map(location=[48.476165, -123.332778], zoom_start=12)

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
                        if vehicle_status == 'IN_TRANSIT_TO':
                            icon = folium.Icon(color='blue', icon='arrow')
                        else:
                            icon = folium.Icon(color='red', icon='arrow')
                        folium.Marker([latitude, longitude],
                          icon=icon, 
                            popup=f"Vehicle ID: {vehicle['vehicle']['id']}\nRoute ID: {route_id}").add_to(m)

            timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            folium.Marker([48.511443, -123.208775], icon=folium.DivIcon(html=f"<div style='font-size: 12pt; font-weight: bold'>Last Updated: {timestamp}</div>"
                                                                         )).add_to(m)  

            # Save map to an HTML file
            temp_path = os.path.join(os.getcwd(), 'vehicle_positions_map.html')
            m.save(temp_path)
            os.rename(temp_path, html_path)

            print(f"Saved map to {html_path}")

            time.sleep(30)

        except Exception as e:
            print(f"Error updating map: {e}")

if __name__ == "__main__":
    html_path = os.path.join(os.getcwd(), 'vehicle_positions_map.html')
    update_map('gtfs_realtime.json')

