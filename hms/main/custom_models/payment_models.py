from django.db import models
from django.dispatch import receiver
from .user_models import *
from django.db.models.signals import post_save

class Passbook(models.Model):
    student = models.OneToOneField(Student, on_delete = models.CASCADE, related_name = "passbook", blank = False, primary_key = True, unique = True)

    def _str_(self):
        return "Passbook: " + self.student.client.first_name + " " + self.student.client.last_name + " - " + self.student.client.stakeholderID


class Payments(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="student_payment")
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)

class StudentPayment(models.Model):
    timestamp = models.DateTimeField("Timestamp", blank = False, auto_now_add = True)
    fulfilled = models.DecimalField("Fulfilled", blank = False, default = 0, max_digits = 8, decimal_places = 2)
    passbook = models.ForeignKey(Passbook, on_delete = models.CASCADE, related_name = "payments")

class Due(models.Model):    
    TYPE = [
        ('mess', 'Mess Dues'),
        ('hostel', 'Hostel Dues'),
        ('amenity', 'Amenity Dues'),
    ]
    
    timestamp = models.DateTimeField("Timestamp", blank = False, auto_now_add = True)
    demand = models.DecimalField("Demand", blank = False, default = 0, max_digits = 8, decimal_places = 2)
    type = models.CharField("Type", max_length = 100, choices = TYPE, blank = False, default = 'mess')
    passbook = models.ForeignKey(Passbook, on_delete = models.CASCADE, related_name = "dues", blank = False)
    
    def __str__(self):
        return  self.type + ":" + self.passbook.student.client.first_name + " " + self.passbook.student.client.last_name + " - " + self.passbook.student.client.stakeholderID

