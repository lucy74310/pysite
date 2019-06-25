from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'main/index.html')


def bad_request(request):
    return render(request, 'errer/400.html', status=400)


def page_not_found(request):
    return render(request, 'errer/404.html', status=404)


def server_error(request):
    return render(request, 'errer/500.html', status=500)

