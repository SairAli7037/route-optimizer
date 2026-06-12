import time

from django.core.management.base import BaseCommand

from geopy.geocoders import Nominatim

from route_optimizer.models import (
    FuelStation,
    CityCoordinate
)


class Command(BaseCommand):

    help = "Enrich city coordinates"

    def handle(self, *args, **kwargs):

        geolocator = Nominatim(
            user_agent="spotter_project"
        )

        unique_locations = (
            FuelStation.objects
            .values("city", "state")
            .distinct()
        )

        created = 0
        failed = 0

        for location in unique_locations:

            city = location["city"]
            state = location["state"]

            exists = CityCoordinate.objects.filter(
                city=city,
                state=state
            ).exists()

            if exists:
                continue

            try:

                query = f"{city}, {state}"

                result = geolocator.geocode(
                    query,
                    timeout=10
                )

                if result:

                    CityCoordinate.objects.create(
                        city=city,
                        state=state,
                        latitude=result.latitude,
                        longitude=result.longitude
                    )

                    created += 1

                else:
                    failed += 1

                time.sleep(1)

            except Exception:

                failed += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Created={created}, Failed={failed}"
            )
        )