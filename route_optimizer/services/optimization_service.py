import math


class OptimizationService:

    VEHICLE_RANGE_MILES = 500
    MPG = 10

    @classmethod
    def calculate_trip_requirements(cls, distance_miles):

        fuel_needed_gallons = distance_miles / cls.MPG

        fuel_stops_needed = max(
            0,
            math.ceil(distance_miles / cls.VEHICLE_RANGE_MILES) - 1
        )

        return {
            "distance_miles": round(distance_miles, 2),
            "fuel_needed_gallons": round(fuel_needed_gallons, 2),
            "fuel_stops_needed": fuel_stops_needed,
        }