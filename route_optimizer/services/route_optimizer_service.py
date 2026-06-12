from route_optimizer.services.routing_service import RoutingService
from route_optimizer.services.station_service import StationService
from route_optimizer.services.fuel_optimizer import FuelOptimizer
from route_optimizer.services.cost_service import CostService


class RouteOptimizerService:

    @classmethod
    def optimize(cls, start, end):

        route = RoutingService.get_route(
            start,
            end
        )

        trip_distance = round(
            route["routes"][0]["summary"]["distance"] / 1609.34,
            2
        )

        route_geometry = (
            route["routes"][0]["geometry"]
        )

        route_points = RoutingService.get_route_points(
            start,
            end
        )

        cumulative_distances = (
            RoutingService.get_cumulative_route_distances(
                start,
                end
            )
        )

        sampled_points = (
            RoutingService.get_sampled_route_points(
                start,
                end
            )
        )

        nearby_stations = (
            StationService.find_near_route(
                sampled_points
            )
        )

        ordered_stations = (
            FuelOptimizer.sort_stations_along_route(
                nearby_stations,
                sampled_points,
                StationService
            )
        )

        for station in ordered_stations:

            route_index = (
                StationService.get_station_route_index(
                    station,
                    sampled_points
                )
            )

            route_index = min(
                route_index * 200,
                len(cumulative_distances) - 1
            )

            station.route_mile = (
                cumulative_distances[route_index]
            )

        fuel_stops = (
            FuelOptimizer.select_fuel_stops(
                ordered_stations,
                trip_distance
            )
        )

        total_cost = (
            CostService.calculate_fuel_cost(
                fuel_stops
            )
        )

        fuel_needed = round(
            trip_distance / 10,
            2
        )

        return {
            "distance_miles": trip_distance,

            "fuel_needed_gallons": fuel_needed,

            "candidate_station_count": len(
                ordered_stations
            ),

            "fuel_stop_count": len(
                fuel_stops
            ),

            "fuel_stops": fuel_stops,

            "total_fuel_cost": total_cost,

            "route_geometry": route_geometry,

            "start": {
                "latitude": start[0],
                "longitude": start[1]
            },
            
            "end": {
                "latitude": end[0],
                "longitude": end[1]
            }
        }