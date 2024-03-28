from django.db import models
from .entity_models import Hall
from .user_models import Student, HallEmployee
from datetime import datetime


class Notice(models.Model):
    title = models.CharField(max_length=200, blank=False, default="")
    content = models.TextField(default="")
    date_created = models.DateTimeField(default=datetime.now)
    image = models.ImageField(
        upload_to="uploads/",
        default="default.jpg",
        height_field=None,
        width_field=None,
        max_length=100,
    )
    hall = models.ForeignKey(
        Hall, related_name="hall_notices", on_delete=models.CASCADE, default=None
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Notices"


class Complaint(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(default="")
    date_created = models.DateField(default=datetime.now)
    image = models.ImageField(
        upload_to="uploads/",
        default="default.jpg",
        height_field=None,
        width_field=None,
        max_length=100,
    )
    hall = models.ForeignKey(
        Hall, default=None, related_name="hall_complaints", on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        Student,
        related_name="student_complaints",
        on_delete=models.CASCADE,
        default=None,
    )
    status = models.BooleanField(default=False)
    CATEGORY = [
        ("maintenance", "Maintenance"),
        ("mess", "Mess"),
        ("room condition", "Room Condition"),
        ("plumbing", "plumbing"),
        ("health", "Health"),
    ]

    category = models.CharField(
        "Category", max_length=40, choices=CATEGORY, default="maintenance", blank=False
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Complaint"


class ATR(models.Model):
    complaint = models.OneToOneField(
        Complaint,
        on_delete=models.CASCADE,
        related_name="complaint",
        primary_key=True,
        blank=False,
        unique=True,
    )

    employee = models.ForeignKey(
        HallEmployee,
        related_name="assigned_employee",
        on_delete=models.CASCADE,
        blank=False,
        default=None,
    )

    report = models.TextField(default="No Action Taken")
