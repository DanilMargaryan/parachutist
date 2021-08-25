from django.http import response, HttpResponse, Http404
from django.shortcuts import render
from main import models
import datetime

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

def add_new_review(request):
    if request.method == 'POST':
        review = models.Review.objects.create()
        review.name = request.POST['name']
        review.email = request.POST['email']
        review.rating = request.POST['rating']
        review.save()
        return HttpResponse('1')
    return HttpResponse('0')

# DELETE IT IF OTHER DEF WORK
# def dynamic_lookup_view(request, book_id):
#     obj = Room.objects.get(id=book_id)
#     context = {
#         "object": obj
#     }
#     return render(request, 'main/index.html', context)

def dynamic_lookup_view(request, book_id):
    try:
        offset = int(book_id)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)