from django.db import models


class Room(models.Model):
    room_number = models.IntegerField()
    room_type = models.CharField(max_length=100)
    booked = models.BooleanField()
    name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)


