from geopy.distance import geodesic
from route_optimizer.models import FuelStation
from math import radians, sin, cos, sqrt, atan2


class StationService:

    @classmethod
    def get_candidate_stations(cls):
        return FuelStation.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False
        )
    
    @staticmethod
    def haversine_miles(point1, point2):
    
        lat1, lon1 = point1
        lat2, lon2 = point2
    
        r = 3958.8
    
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
    
        a = (
            sin(dlat / 2) ** 2
            +
            cos(radians(lat1))
            *
            cos(radians(lat2))
            *
            sin(dlon / 2) ** 2
        )
    
        c = 2 * atan2(
            sqrt(a),
            sqrt(1 - a)
        )
    
        return r * c
    


    @classmethod
    def find_near_route(
        cls,
        sampled_points,
        max_distance_miles=25
    ):

        stations = cls.get_candidate_stations()

        nearby_stations = []

        for station in stations:

            station_point = (
                station.latitude,
                station.longitude
            )

            for route_point in sampled_points:

                distance = cls.haversine_miles(
                station_point,
                route_point
            )

                if distance <= max_distance_miles:

                    nearby_stations.append(station)

                    break

        return nearby_stations
    
    

    @classmethod
    def get_station_route_index(
        cls,
        station,
        sampled_points
    ):

        station_point = (
            station.latitude,
            station.longitude
        )
    
        closest_index = None
        closest_distance = float("inf")
    
        for idx, route_point in enumerate(sampled_points):
    
            distance = cls.haversine_miles(
            station_point,
            route_point
        )
    
            if distance < closest_distance:
    
                closest_distance = distance
                closest_index = idx
    
        return closest_index
    

    @classmethod
    def get_station_route_mile(
        cls,
        station,
        route_points,
        cumulative_distances
    ):
        station_point = (
            station.latitude,
            station.longitude
    
        )
        closest_index = None
        closest_distance = float("inf")
        for idx, route_point in enumerate(route_points):
    
    
            station_point,
            distance = geodesic(
                route_point
    
            ).miles
    
            if distance < closest_distance:
                closest_distance = distance
                closest_index = idx
    
        return cumulative_distances[closest_index]
    

    