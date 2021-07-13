from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    pass

class Time(models.Model):
    time = models.CharField(max_length=64)

    def __str__ (self):
        return f"{self.time}"

class Medicine(models.Model):
    time = models.ForeignKey(Time, related_name="time_of_day", on_delete=models.CASCADE)
    name = models.CharField(max_length = 64)
    taken = models.BooleanField(default=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField()

    def __str__ (self):
        return f"[{self.name}] under [{self.time}]"
