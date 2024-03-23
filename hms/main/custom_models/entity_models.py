from django.db import models
from datetime import datetime


class Hall(models.Model):
    name = models.CharField("Name", max_length=20, blank=False, unique=True)
    max_occupancy = models.IntegerField("max_occupancy", blank=False, default=0)
    current_occupancy = models.IntegerField("current_occupancy", blank=False, default=0)
    no_of_rooms = models.IntegerField("no_of_rooms", blank=False, default=0)

    def __str__(self):
        return self.name


class Amenities(models.Model):
    name = models.CharField("Amenity_Name", max_length=50, blank=True)
    hall = models.ForeignKey(
        Hall, on_delete=models.CASCADE, related_name="hall_amenity"
    )
    established_date = models.DateField(default=datetime.now, blank=False)
    total_price = models.IntegerField("amenity_price", default=0, blank=True)
