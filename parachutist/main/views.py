from django.shortcuts import render
from main import models


def index(request):
    return render(request, 'main/index.html')


def gallery(request):
    return render(request, 'gallery.html')


def services(request):
    return render(request, 'services.html')


def booking(request):
    args = {
        'rooms': models.Room.objects.all()
    }
    return render(request, 'booking.html', args)


def debtors(request):
    args = {
        'lohs': models.Debtor.objects.all()
    }
    return render(request, 'developers.html', args)
