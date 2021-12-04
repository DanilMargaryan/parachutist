from django.http import response, HttpResponse
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
        'rooms': models.RoomType.objects.all()
    }
    return render(request, 'booking.html', args)


def debtors(request):
    args = {
        'lohs': models.Debtor.objects.all()
    }
    return render(request, 'developers.html', args)


def add_new_review(request):
    if request.method == 'POST':
        review = models.Review.objects.create()
        review.name = request.POST['name']
        review.email = request.POST['email']
        review.rating = request.POST['rating']
        review.save()
        return HttpResponse('1')
    return HttpResponse('0')
