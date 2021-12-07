import json
from datetime import datetime

import pytz
from django.http import response, HttpResponse
from django.shortcuts import render, redirect
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

    if request.method == 'POST':
        range_date_form = forms.RangeDate(request.POST)
        if range_date_form.is_valid():
            if range_date_form.cleaned_data['start_date'] is not None:
                start_date = range_date_form.cleaned_data['start_date']
            if range_date_form.cleaned_data['end_date'] is not None:
                end_date = range_date_form.cleaned_data['end_date']
            if 'rooms' in request.POST:
                request.session['rooms'] = json.loads(request.POST['rooms'])
                return redirect(f'/booking/order?start_date={request.POST["start_date"]}'
                                f'&end_date={request.POST["end_date"]}')
    else:
        range_date_form = forms.RangeDate()
    overlapping_orders = models.BookedRoom.get_overlapping_orders_by_date(models.BookedRoom.objects, start_date, end_date)
    # rooms = models.BookedRoom.objects.exclude(id__in=overlapping_orders)

    rooms_types = zip(models.RoomType.objects.all(),
                      [rt.count - rt.get_rooms(overlapping_orders).count() for rt in models.RoomType.objects.all()])

    args = {
        'room_types': rooms_types,
        'range_date_form': range_date_form,
    }
    return render(request, 'booking.html', args)


def booking_order(request):
    rooms_selected = []
    order_room_form = forms.OrderRoom()

    if 'rooms' in request.session:
        rooms_count = request.session['rooms']
        for room_type in models.RoomType.objects.filter(id__in=rooms_count.keys()):
            rooms_selected.append({
                'room': room_type,
                'count': rooms_count[str(room_type.id)]
            })

    if request.method == 'GET':
        order_room_form = forms.OrderRoom(request.GET)
    elif request.method == 'POST':
        order_room_form = forms.OrderRoom(request.POST)
        if order_room_form.is_valid():
            for room_type_id in rooms_count:
                room_type = models.RoomType.objects.get(id=room_type_id)
                for _ in range(rooms_count[room_type_id]):
                    models.BookedRoom.objects.create(start_date=order_room_form.cleaned_data['start_date'],
                                                     end_date=order_room_form.cleaned_data['end_date'],
                                                     name=order_room_form.cleaned_data['name'],
                                                     last_name=order_room_form.cleaned_data['last_name'],
                                                     phone=order_room_form.cleaned_data['phone'],
                                                     email=order_room_form.cleaned_data['email'],
                                                     room_type=room_type)
            return redirect('/booking/success')

    args = {
        'rooms_selected': rooms_selected,
        'order_room_form': order_room_form,
    }
    return render(request, 'booking-order.html', args)


def booking_success(request):
    return render(request, 'booking-success.html')


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
