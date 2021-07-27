import os.path
import urllib

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files import File


class Room(models.Model):
    room_number = models.IntegerField()
    room_type = models.CharField(max_length=100)
    booked = models.BooleanField()
    name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)


class Debtor(models.Model):
    name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    link = models.CharField(max_length=512)
    photo = models.ImageField(default='img/8901.jpg', upload_to='img')

class Review(models.Model):
    text = models.TextField()
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])