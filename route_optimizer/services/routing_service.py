import os
import requests
import polyline
from geopy.distance import geodesic



class RoutingService:

    BASE_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

    @classmethod
    def get_route(cls, start, end):

        headers = {
            "Authorization": os.getenv("ORS_API_KEY"),
            "Content-Type": "application/json",
        }

        body = {
            "coordinates": [
                [start[1], start[0]],  # lon, lat
                [end[1], end[0]]
            ]
        }

        response = requests.post(
            cls.BASE_URL,
            json=body,
            headers=headers,
            timeout=30
        )

        print(response.status_code)

        response.raise_for_status()

        return response.json()
    

    @classmethod
    def get_route_points(cls, start, end):
        route = cls.get_route(start, end)

        geometry = route["routes"][0]["geometry"]

        return polyline.decode(geometry)

    @classmethod
    def get_sampled_route_points(
        cls,
        start,
        end,
        sample_step=200
    ):
        points = cls.get_route_points(start, end)

        return points[::sample_step]
    

    @classmethod
    def get_cumulative_route_distances(
        cls,
        start,
        end
    ):
        points = cls.get_route_points(start, end)
    
        cumulative = [0]
    
        total = 0
    
        for i in range(1, len(points)):
    
            total += geodesic(
                points[i - 1],
                points[i]
            ).miles
    
            cumulative.append(total)
    
        return cumulative