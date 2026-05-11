def emit_data():
    routes_data = {}

    try:
        with open('routes.json', 'r') as json_file:
            routes_data = json.load(json_file)
            routes_dict = {route['route_id']: route['headsign'] for route in routes_data}
    except Exception as e:
        print(f"Error loading data route {e}")


    while True:
        try:
            with open('gtfs_realtime.json', 'r') as json_file:
                feed_dict = json.load(json_file)

                socketio.emit('vehicle_update', feed_dict)
                # Add vehicle positions to the map
                for entity in feed_dict['entity']:
                    if 'vehicle' in entity:
                        vehicle = entity['vehicle']
                        position = vehicle.get('position', {})
                        latitude = position.get('latitude')
                        longitude = position.get('longitude')
                        if latitude and longitude:
                            route_id = vehicle.get('trip', {}).get('routeId', 'N/A')
                            vehicle_id = vehicle.get('vehicle', {}).get('id', 'UNKNOWN')
                            vehicle_status = vehicle.get('currentStatus', 'UNKNOWN')
                            vehicle_seats = vehicle.get('occupancyStatus', 'UNKNOWN')
                            vehicle_speed = vehicle.get('speed', 'UNKNOWN')
                            headsign = routes_dict.get(route_id, 'UNKNOWN')
                            if vehicle_speed is None:
                                vehicle_speed = 'Speed not available'
                            socketio.emit('vehicle_update', {
                                'latitude' : latitude,
                                'longitude' : longitude,
                                'route_id': route_id,
                                'vehicle_id': vehicle_id,
                                'vehicle_status': vehicle_status,
                                'vehicle_seats': vehicle_seats,
                                'vehicle_speed': vehicle_speed,
                                'headsign' : headsign
                                })
            
            
                            
            # with open('routes.json', 'r') as json_file:
            #     data_route = json.load(json_file)
            #     socketio.emit('route', data_route)

                # for route in data_route:
                #     shape_id = route.get('shape_id')
                #     route_id1 = route.get('route_id')
                #     headsign = route.get('headsign')
                #     socketio.emit('route', {
                #         'shape_id' : shape_id,
                #         'route_id': route_id1,
                #         'headsign': headsign
                #     })
            time.sleep(5)

        except Exception as e:
            print(f"Error updating map: {e}")


