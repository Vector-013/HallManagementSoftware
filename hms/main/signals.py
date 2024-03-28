from django.dispatch import receiver
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=Student)
def create_student_payment(sender, instance, created, **kwargs):
    if created:
        Payments.objects.create(student=instance)


@receiver(post_save, sender=Student)
def create_passbook(sender, instance, created, **kwargs):
    if created:
        StudentPassbook.objects.create(student=instance)
