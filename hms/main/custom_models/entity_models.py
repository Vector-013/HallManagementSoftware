from django.db import models
from datetime import datetime


class Hall(models.Model):
    name = models.CharField("Name", max_length=20, blank=False, unique=True)
    max_occupancy = models.IntegerField("Max Occupancy", blank=False, default=0)
    current_occupancy = models.IntegerField("Current Occupancy", blank=False, default=0)
    blocks = models.IntegerField("Number of blocks", blank=False, default=0)
    floors = models.IntegerField("Floors per block", blank=False, default=0)
    singles = models.IntegerField("Single Rooms per floor", blank=False, default=0)
    doubles = models.IntegerField("Double Rooms per floor", blank=False, default=0)
    triples = models.IntegerField("Triple Rooms per floor", blank=False, default=0)

    def calculate_max_occupancy(self):
        rooms = Room.objects.filter(hall=self)
        total = 0
        for room in rooms:
            total += room.sharing
        return total

    def calculate_curr_occupancy(self):
        rooms = Room.objects.filter(hall=self)
        total = 0
        for room in rooms:
            total += room.current_occupancy
        return total

    def __str__(self):
        return self.name


class Amenities(models.Model):
    name = models.CharField("Amenity Name", max_length=50, blank=True)
    hall = models.ForeignKey(
        Hall, on_delete=models.CASCADE, related_name="hall_amenity"
    )
    established_date = models.DateField(default=datetime.now, blank=False)
    total_price = models.IntegerField("Amenity Price", default=0, blank=True)


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
            ("January", "January"),
            ("Febraury", "February"),
            ("March", "March"),
            ("April", "April"),
            ("May", "May"),
            ("June", "June"),
            ("July", "July"),
            ("August", "August"),
            ("September", "September"),
            ("October", "October"),
            ("November", "November"),
            ("December", "December"),
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
    qt1 = models.IntegerField("Quantity 1", blank=True)
    rate1 = models.IntegerField("Rate 1", blank=True)

    item2 = models.CharField("Item 2", max_length=20, blank=True)
    qt2 = models.IntegerField("Quantity 2", blank=True)
    rate2 = models.IntegerField("Rate 2", blank=True)

    item3 = models.CharField("Item 3", max_length=20, blank=True)
    qt3 = models.IntegerField("Quantity 3", blank=True)
    rate3 = models.IntegerField("Rate 3", blank=True)

    item4 = models.CharField("Item 4", max_length=20, blank=True)
    qt4 = models.IntegerField("Quantity 4", blank=True)
    rate4 = models.IntegerField("Rate 4", blank=True)

    item5 = models.CharField("Item 5", max_length=20, blank=True)
    qt5 = models.IntegerField("Quantity 5", blank=True)
    rate5 = models.IntegerField("Rate 5", blank=True)

    total = models.IntegerField("total", blank=True)


class Room(models.Model):
    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        related_name="hall_room",
        default=None,
    )
    current_occupancy = models.IntegerField("Current Occupancy", blank=False, default=0)
    is_free = models.BooleanField("Status", default=True, blank=False)
    rent = models.DecimalField(
        "Rent", blank=False, default=5000, max_digits=10, decimal_places=2
    )
    sharing = models.IntegerField(
        "Sharing",
        choices=[(1, "1"), (2, "2"), (3, "3")],
    )
    floor = models.IntegerField("Floor", blank=False, default=0)
    block = models.CharField("Block", max_length=1, blank=False, default="A")
    number = models.IntegerField("Room Number", blank=False, default=0)

    code = models.CharField(
        "Code", blank=False, default=None, primary_key=True, max_length=100
    )

    def check_room(self):
        if self.hall.floor <= self.room.floor and self.hall.block <= self.room.block:
            return True
        else:
            return False
