from django.shortcuts import render


def test(request):
    args = {'address': 'my address'}
    return render(request, 'main/index.html', args)
