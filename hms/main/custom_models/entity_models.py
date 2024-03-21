from django.db import models


class Hall(models.Model):
    name = models.CharField("Name", max_length=20, blank=False, unique=True)
    max_occupancy = models.IntegerField("max_occupancy", blank=False, default=0)
    current_occupancy = models.IntegerField("current_occupancy", blank=False, default=0)
    no_of_rooms = models.IntegerField("no_of_rooms", blank=False, default=0)

    def __str__(self):
        return self.name
