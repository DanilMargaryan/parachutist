import json
from datetime import datetime

import pytz
from django.http import response, HttpResponse
from django.shortcuts import render, redirect
from main import models, forms
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from parachutist import settings


def index(request):
    range_date = forms.RangeDate()
    range_date.fields['start_date'].widget.attrs['class'] = 'top__calendar-input'
    range_date.fields['end_date'].widget.attrs['class'] = 'top__calendar-input'
    args = {
        'range_date': range_date
    }
    return render(request, 'main/index.html', args)


def gallery(request, img_type):
    args = {
        'imgs': models.Gallery.objects.filter(type=img_type)
    }
    return render(request, 'gallery.html', args)


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

    args = {
        'rooms_selected': rooms_selected,
    }

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
        args['order_room_form'] = order_room_form
        if order_room_form.is_valid():
            overlapping_orders = models.BookedRoom.get_overlapping_orders_by_date(models.BookedRoom.objects,
                                                                                  order_room_form.cleaned_data['start_date'],
                                                                                  order_room_form.cleaned_data['end_date'])
            for room_type_id in rooms_count:
                rooms_left = room_type.count - room_type.get_rooms(overlapping_orders).count()
                if rooms_left < rooms_count[room_type_id]:
                    return render(request, 'booking-failure.html', args)

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
            html_email = render_to_string('email_send.html', args)
            text_content = strip_tags(html_email)
            email = EmailMultiAlternatives('Успешно забронировано',
                                           text_content,
                                           settings.EMAIL_HOST_USER,
                                           [order_room_form.cleaned_data['email']])
            email.attach_alternative(html_email, 'text/html')
            email.send()
            return render(request, 'booking-success.html', args)
        else:
            for field in order_room_form.errors:
                order_room_form[field].field.widget.attrs['class'] += ' ' + order_room_form.error_css_class

    args['order_room_form'] = order_room_form
    return render(request, 'booking-order.html', args)


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
