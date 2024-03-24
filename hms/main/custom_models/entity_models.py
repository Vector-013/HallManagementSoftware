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


class Menu(models.Model):
    hall = models.OneToOneField(
        Hall,
        on_delete=models.CASCADE,
        related_name="hall_menu",
        default=None,
        primary_key=True,
    )
    month = models.CharField(
        "Month",
        max_length=20,
        choices=[
            ("jan", "January"),
            ("feb", "February"),
            ("mar", "March"),
            ("apr", "April"),
            ("may", "May"),
            ("jun", "June"),
            ("jul", "July"),
            ("aug", "August"),
            ("sep", "September"),
            ("oct", "October"),
            ("nov", "November"),
            ("dec", "December"),
        ],
    )
    monday_breakfast = models.CharField("Monday Breakfast", max_length=50, default="A")
    monday_lunch = models.CharField("Monday Lunch", max_length=50, default="B")
    monday_snacks = models.CharField("Monday Snacks", max_length=50, default="C")
    monday_dinner = models.CharField("Monday Dinner", max_length=50, default="D")
    tuesday_breakfast = models.CharField(
        "Tuesday Breakfast", max_length=50, default="E"
    )
    tuesday_lunch = models.CharField("Tuesday Lunch", max_length=50, default="A1")
    tuesday_snacks = models.CharField("Tuesday Snacks", max_length=50, default="F")
    tuesday_dinner = models.CharField("Tuesday Dinner", max_length=50, default="G")
    wednesday_breakfast = models.CharField(
        "Wednesday Breakfast", max_length=50, default="H"
    )
    wednesday_lunch = models.CharField("Wednesday Lunch", max_length=50, default="I")
    wednesday_snacks = models.CharField("Wednesday Snacks", max_length=50, default="J")
    wednesday_dinner = models.CharField("Wednesday Dinner", max_length=50, default="K")
    thursday_breakfast = models.CharField(
        "Thursday Breakfast", max_length=50, default="J1"
    )
    thursday_lunch = models.CharField("Thursday Lunch", max_length=50, default="L")
    thursday_snacks = models.CharField("Thursday Snacks", max_length=50, default="M")
    thursday_dinner = models.CharField("Thursday Dinner", max_length=50, default="N")
    friday_breakfast = models.CharField("Friday Breakfast", max_length=50, default="O")
    friday_lunch = models.CharField("Friday Lunch", max_length=50, default="P")
    friday_snacks = models.CharField("Friday Snacks", max_length=50, default="Q")
    friday_dinner = models.CharField("Friday Dinner", max_length=50, default="R")
    saturday_breakfast = models.CharField(
        "Saturday Breakfast", max_length=50, default="S"
    )
    saturday_lunch = models.CharField("Saturday Lunch", max_length=50, default="T")
    saturday_snacks = models.CharField("Saturday Snacks", max_length=50, default="U")
    saturday_dinner = models.CharField("Saturday Dinner", max_length=50, default="V")
    sunday_breakfast = models.CharField("Sunday Breakfast", max_length=50, default="W")
    sunday_lunch = models.CharField("Sunday Lunch", max_length=50, default="X")
    sunday_snacks = models.CharField("Sunday Snacks", max_length=50, default="Y")
    sunday_dinner = models.CharField("Sunday Dinner", max_length=50, default="Z")


class Ration(models.Model):
    hall = models.OneToOneField(
        Hall,
        on_delete=models.CASCADE,
        related_name="hall_ration",
        default=None,
        primary_key=True,
    )

    item1 = models.CharField("Item 1", max_length=20, blank=True)
    qt1 = models.IntegerField("qt1", blank=True)
    rate1 = models.IntegerField("rt1", blank=True)

    item2 = models.CharField("Item ", max_length=20, blank=True)
    qt2 = models.IntegerField("qt2", blank=True)
    rate2 = models.IntegerField("rt2", blank=True)

    item3 = models.CharField("Item 3", max_length=20, blank=True)
    qt3 = models.IntegerField("qt3", blank=True)
    rate3 = models.IntegerField("rt3", blank=True)

    item4 = models.CharField("Item 4", max_length=20, blank=True)
    qt4 = models.IntegerField("qt4", blank=True)
    rate4 = models.IntegerField("rt4", blank=True)

    item5 = models.CharField("Item 5", max_length=20, blank=True)
    qt5 = models.IntegerField("qt5", blank=True)
    rate5 = models.IntegerField("rt5", blank=True)

    total = models.IntegerField("total", blank=True)


class Room(models.Model):
    hall = models.ForeignKey(
        Hall, on_delete=models.CASCADE, related_name="hall_room", default=None
    )
