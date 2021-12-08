import os.path
import urllib

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files import File
from django.db.models import Q


class RoomType(models.Model):
    room_type = models.CharField(max_length=100)
    count = models.IntegerField()
    price = models.FloatField()
    price_for_3_nights = models.FloatField()
    capacity = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.room_type

    def get_rooms(self, rooms):
        return rooms.filter(room_type=self)

    @property
    def images(self):
        return ImageRoom.objects.filter(room_type=self)


class BookedRoom(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)

    @staticmethod
    def get_overlapping_orders_by_date(activities, start_date, end_date):
        return activities.filter(
            Q(start_date__lte=start_date) & Q(end_date__gte=start_date) |
            Q(start_date__lte=end_date) & Q(end_date__gte=end_date) |
            Q(start_date__range=(start_date, end_date))
        )

    def get_overlapping_orders(self):
        return BookedRoom.get_overlapping_orders_by_date(BookedRoom.objects, self.start_date, self.end_date)

    def __str__(self):
        return f'{self.room_type.room_type} {self.last_name}'


class ImageRoom(models.Model):
    image = models.ImageField(upload_to='img', null=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery', null=True)
    type = models.CharField(max_length=100)

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