from django.db import models


class User(models.Model):
    name = models.CharField(max_length=8, default="")
    score = models.IntegerField(null=False, default=666)
    alive = models.BooleanField(null=False, default=False)
