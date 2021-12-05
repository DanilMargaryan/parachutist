from datetime import datetime

import pytz
from django.http import response, HttpResponse
from django.shortcuts import render
from main import models, forms


def index(request):
    return render(request, 'main/index.html')


def gallery(request):
    return render(request, 'gallery.html')


def services(request):
    return render(request, 'services.html')


def booking(request):
    start_date = datetime.today()
    end_date = datetime(2999, 11, 20, tzinfo=pytz.UTC)

    if request.method == 'GET':
        range_date_form = forms.RangeDate(request.GET)
        if range_date_form.is_valid():
            if range_date_form.cleaned_data['start_date'] is not None:
                start_date = range_date_form.cleaned_data['start_date']
            if range_date_form.cleaned_data['end_date'] is not None:
                end_date = range_date_form.cleaned_data['end_date']
    else:
        range_date_form = forms.RangeDate()
    overlapping_orders = models.Room.get_overlapping_orders_by_date(models.Room.objects, start_date, end_date)
    rooms = models.Room.objects.exclude(id__in=overlapping_orders)

    rooms_types = zip(models.RoomType.objects.all(),
                      [rt.get_rooms(rooms) for rt in models.RoomType.objects.all()])

    args = {
        'room_types': rooms_types,
        'range_date_form': range_date_form,
    }
    return render(request, 'booking.html', args)


def debtors(request):
    args = {
        'lohs': models.Debtor.objects.all(),
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
