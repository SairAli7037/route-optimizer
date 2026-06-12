import pandas as pd

from django.core.management.base import BaseCommand

from route_optimizer.models import FuelStation


class Command(BaseCommand):
    help = "Import fuel stations from CSV"

    def handle(self, *args, **kwargs):

        csv_path = "data/fuel-prices-for-be-assessment.csv"

        df = pd.read_csv(csv_path)

        FuelStation.objects.all().delete()

        stations = []

        for _, row in df.iterrows():

            stations.append(
                FuelStation(
                    truckstop_id=row["OPIS Truckstop ID"],
                    truckstop_name=row["Truckstop Name"],
                    address=row["Address"],
                    city=row["City"],
                    state=row["State"],
                    rack_id=row["Rack ID"],
                    retail_price=row["Retail Price"],
                )
            )

        FuelStation.objects.bulk_create(
            stations,
            batch_size=1000
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported {len(stations)} stations successfully."
            )
        )