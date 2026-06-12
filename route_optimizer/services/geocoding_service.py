import os
import requests


class GeocodingService:

    BASE_URL = (
        "https://api.openrouteservice.org/geocode/search"
    )

    @classmethod
    def get_coordinates(
        cls,
        city_name
    ):

        headers = {
            "Authorization":
                os.getenv("ORS_API_KEY")
        }

        params = {
            "text": city_name,
            "size": 1
        }

        response = requests.get(
            cls.BASE_URL,
            headers=headers,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if not data["features"]:
            raise ValueError(
                f"City not found: {city_name}"
            )
        
        coordinates = (
            data["features"][0]
            ["geometry"]
            ["coordinates"]
        )
        
        return (
            coordinates[1],
            coordinates[0]
        )