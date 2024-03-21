from django.db import models
from .entity_models import Hall
from .user_models import Student
from datetime import datetime


class Notice(models.Model):
    title = models.CharField(max_length=200, blank=False, default="")
    content = models.TextField(default="")
    date_created = models.DateTimeField(default=datetime.now)
    image = models.ImageField(
        height_field=None,
        width_field=None,
        max_length=100,
    )
    hall = models.ForeignKey(
        Hall, related_name="hall_notices", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Notices"


class Complaint(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(default="")
    date_created = models.DateField(default=datetime.now)
    hall = models.ForeignKey(
        Hall, related_name="hall_complaints", on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        Student, related_name="student_complaints", on_delete=models.CASCADE
    )

    ROLES = [
        ("maintenance", "Maintenance"),
        ("mess", "Mess"),
        ("room condition", "Room Condition"),
        ("plumbing", "plumbing"),
        ("health", "Health"),
    ]

    role = models.CharField(
        "Role", max_length=40, choices=ROLES, default="maintenance", blank=False
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Complaint"


class Dues(models.Model):
    pass
