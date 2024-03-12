from django.db import models
from django.http import HttpResponse

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=8, default="")
    score = models.IntegerField(null=False, default=666)
    alive = models.BooleanField(null=False, default=False)
