from django.db import models
from django.dispatch import receiver
from .user_models import *
from django.db.models.signals import post_save


class StudentPassbook(models.Model):
    student = models.OneToOneField(
        Student,
        on_delete=models.CASCADE,
        related_name="student_passbook",
        blank=False,
        primary_key=True,
        unique=True,
    )

    def _str_(self):
        return (
            "Student Passbook: "
            + self.student.client.first_name
            + " "
            + self.student.client.last_name
            + " - "
            + self.student.client.stakeholderID
        )


class Payments(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="payments"
    )
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)


class StudentPayment(models.Model):
    timestamp = models.DateTimeField("Timestamp", blank=False, auto_now_add=True)
    fulfilled = models.DecimalField(
        "Fulfilled", blank=False, default=0, max_digits=8, decimal_places=2
    )
    student_passbook = models.ForeignKey(
        StudentPassbook, on_delete=models.CASCADE, related_name="student_payment"
    )


class Due(models.Model):
    TYPE = [
        ("mess", "Mess Dues"),
        ("hostel", "Hostel Dues"),
        ("amenity", "Amenity Dues"),
    ]

    timestamp = models.DateTimeField("Timestamp", blank=False, auto_now_add=True)
    demand = models.DecimalField(
        "Demand", blank=False, default=0, max_digits=8, decimal_places=2
    )
    type = models.CharField(
        "Type", max_length=100, choices=TYPE, blank=False, default="mess"
    )
    student_passbook = models.ForeignKey(
        StudentPassbook, on_delete=models.CASCADE, related_name="dues", blank=False
    )

    def __str__(self):
        return (
            self.type
            + ":"
            + self.student_passbook.student.client.first_name
            + " "
            + self.student_passbook.student.client.last_name
            + " - "
            + self.student_passbook.student.client.stakeholderID
        )


class WardenPassbook(models.Model):
    hall = models.OneToOneField(
        Hall,
        on_delete=models.CASCADE,
        related_name="warden_passbook",
        blank=False,
        primary_key=True,
        unique=True,
    )
    original_budget = models.DecimalField(
        "original_budget",
        blank=False,
        default=20000000,
        max_digits=10,
        decimal_places=2,
    )
    current_budget = models.DecimalField(
        "current_budget", blank=False, default=20000000, max_digits=10, decimal_places=2
    )

    def _str_(self):
        return "Warden Passbook " + self.hall.name


class WardenTransaction(models.Model):
    TYPE = [
        ("hall_allotment", "Hall Allotment"),
        ("mess_allotment", "Mess Allotment"),
        ("grant", "Grant"),
    ]
    type = models.CharField(
        "Type", max_length=100, choices=TYPE, blank=False, default="salaries"
    )
    timestamp = models.DateTimeField("Timestamp", blank=False, auto_now_add=True)
    amount = models.DecimalField(
        "Amount", blank=False, default=0, max_digits=8, decimal_places=2
    )
    warden_passbook = models.ForeignKey(
        WardenPassbook, on_delete=models.CASCADE, related_name="warden_transaction"
    )


class HallPassbook(models.Model):
    hall = models.OneToOneField(
        Hall,
        on_delete=models.CASCADE,
        related_name="hall_passbook",
        blank=False,
        primary_key=True,
        unique=True,
        default=None,
    )

    def _str_(self):
        return "Hall Passbook " + self.hall.name


class HallTransaction(models.Model):
    TYPE = [
        ("salaries", "Salaries"),
        ("amenities", "Amenities"),
        ("allotment", "Allotment"),
    ]
    type = models.CharField(
        "Type", max_length=100, choices=TYPE, blank=False, default="salaries"
    )
    timestamp = models.DateTimeField("Timestamp", blank=False, auto_now_add=True)
    amount = models.DecimalField(
        "Amount", blank=False, default=0, max_digits=8, decimal_places=2
    )
    hall_passbook = models.ForeignKey(
        HallPassbook, on_delete=models.CASCADE, related_name="hall_transaction"
    )


class MessPassbook(models.Model):
    hall = models.OneToOneField(
        Hall,
        on_delete=models.CASCADE,
        related_name="mess_passbook",
        blank=False,
        primary_key=True,
        unique=True,
        default=None,
    )

    def _str_(self):
        return "Mess Passbook " + self.hall.name


class MessTransaction(models.Model):
    TYPE = [
        ("salaries", "Salaries"),
        ("rations", "Rations"),
        ("allotment", "Allotment"),
    ]
    type = models.CharField(
        "Type", max_length=100, choices=TYPE, blank=False, default="salaries"
    )
    timestamp = models.DateTimeField("Timestamp", blank=False, auto_now_add=True)
    amount = models.DecimalField(
        "Amount", blank=False, default=0, max_digits=8, decimal_places=2
    )
    mess_passbook = models.ForeignKey(
        MessPassbook, on_delete=models.CASCADE, related_name="mess_transaction"
    )
