class CostService:

    MPG = 10

    @classmethod
    def calculate_fuel_cost(
        cls,
        fuel_stops
    ):

        total_cost = 0

        for stop in fuel_stops:

            gallons = stop["distance_miles"] / cls.MPG

            cost = gallons * stop["price"]

            total_cost += cost

        return round(total_cost, 2)