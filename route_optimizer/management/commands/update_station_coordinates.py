from django.core.management.base import BaseCommand

from route_optimizer.models import (
    FuelStation,
    CityCoordinate
)


class Command(BaseCommand):

    help = "Update station coordinates"

    def handle(self, *args, **kwargs):

        city_map = {}

        for city in CityCoordinate.objects.all():

            key = (
                city.city.strip().lower(),
                city.state.strip().lower()
            )

            city_map[key] = (
                city.latitude,
                city.longitude
            )

        stations_to_update = []

        stations = FuelStation.objects.all()

        updated = 0

        for station in stations:

            key = (
                station.city.strip().lower(),
                station.state.strip().lower()
            )

            if key in city_map:

                lat, lon = city_map[key]

                station.latitude = lat
                station.longitude = lon

                stations_to_update.append(station)

                updated += 1

        FuelStation.objects.bulk_update(
            stations_to_update,
            ["latitude", "longitude"],
            batch_size=1000
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Updated {updated} stations"
            )
        )