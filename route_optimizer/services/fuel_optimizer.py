class FuelOptimizer:

    VEHICLE_RANGE_MILES = 500

    @classmethod
    def sort_stations_along_route(
        cls,
        stations,
        sampled_points,
        station_service
    ):

        return sorted(
            stations,
            key=lambda station:
            station_service.get_station_route_index(
                station,
                sampled_points
            )
        )
    
    @classmethod
    def select_fuel_stops(
        cls,
        ordered_stations,
        trip_distance
    ):
    
        fuel_stops = []
    
        current_mile = 0
    
        while current_mile < trip_distance:
    
            target_mile = min(
                current_mile + cls.VEHICLE_RANGE_MILES,
                trip_distance
            )
    
            reachable_stations = []
    
            for station in ordered_stations:
    
                station_mile = getattr(
                    station,
                    "route_mile",
                    None
                )
    
                if station_mile is None:
                    continue
    
                if current_mile <= station_mile <= target_mile:
                    reachable_stations.append(
                        station
                    )
    
            if not reachable_stations:
                break
    
            cheapest_station = min(
                reachable_stations,
                key=lambda station:
                station.retail_price
            )
    
            fuel_stops.append(
    {
        "station":
            cheapest_station.truckstop_name,

        "city":
            cheapest_station.city,

        "price":
            float(
                cheapest_station.retail_price
            ),

        "latitude":
            cheapest_station.latitude,

        "longitude":
            cheapest_station.longitude,
        
        "distance_miles":
            target_mile - current_mile,

        "window_start":
            round(current_mile, 0),

        "window_end":
            round(target_mile, 0)
    }
)
    
            current_mile = target_mile
    
        return fuel_stops