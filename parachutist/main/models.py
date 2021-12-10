import os.path
import urllib

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files import File
from django.db.models import Q
from django.utils.html import escape


class RoomType(models.Model):
    room_type = models.CharField(max_length=100, verbose_name='Тип комнаты')
    count = models.IntegerField(verbose_name='Количество')
    price = models.FloatField(verbose_name='Цена')
    capacity = models.IntegerField(verbose_name='Вместимость')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.room_type

    def get_rooms(self, rooms):
        return rooms.filter(room_type=self)

    @property
    def images(self):
        return ImageRoom.objects.filter(room_type=self)

    class Meta:
        verbose_name_plural = 'Типы комнат'


class BookedRoom(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name='Тип комнаты')
    name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=50, verbose_name='Номер телефона')
    email = models.EmailField()
    start_date = models.DateField(blank=True, verbose_name='Дата заезда')
    end_date = models.DateField(blank=True, verbose_name='Дата выезда')

    class Meta:
        verbose_name_plural = 'Забронированные номера'
        ordering = ('-start_date', 'last_name')

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
    image = models.ImageField(upload_to='img', null=True, verbose_name='Фото')
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, verbose_name='Тип комнаты')

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name_plural = 'Фото комнат'


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery', null=True, verbose_name='Путь')
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name_plural = 'Галерея'

    def image_tag(self):
        return u'<img src="%s">' % escape(self.image.url)


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
