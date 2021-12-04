import os.path
import urllib

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files import File


class RoomType(models.Model):
    room_type = models.CharField(max_length=100)
    price = models.FloatField()
    price_for_3_nights = models.FloatField()
    capacity = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.room_type

    @property
    def free(self):
        return Room.objects.filter(room_type=self, booked=False)

    @property
    def images(self):
        return ImageModel.objects.filter(room_type=self)


class Room(models.Model):
    room_number = models.IntegerField()
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    booked = models.BooleanField()
    name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f'№{self.room_number} {self.room_type.room_type}'


class ImageModel(models.Model):
    image = models.ImageField(upload_to='img', null=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name


class Debtor(models.Model):
    name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    link = models.CharField(max_length=512)
    photo = models.ImageField(default='img/8901.jpg', upload_to='img')


class Review(models.Model):
    text = models.TextField()
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    rating = models.IntegerField()