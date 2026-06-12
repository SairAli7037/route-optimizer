from django.db import models


class FuelStation(models.Model):
    truckstop_id = models.IntegerField()

    truckstop_name = models.CharField(max_length=255)

    address = models.CharField(max_length=500)

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=50)

    rack_id = models.IntegerField()

    retail_price = models.DecimalField(
        max_digits=6,
        decimal_places=3
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.truckstop_name} - {self.city}, {self.state}"
    
    class Meta:
        indexes = [
            models.Index(fields=["state"]),
            models.Index(fields=["city"]),
    ]

class CityCoordinate(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)

    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        unique_together = ("city", "state")