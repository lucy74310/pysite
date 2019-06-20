from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from user.models import User


def joinform(request):
    return render(request, 'user/joinform.html')


def join(request):
    user = User()

    user.name = request.POST['name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.gender = request.POST['gender']

    user.save()

    return HttpResponseRedirect('/user/joinsuccess')


def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')


def loginform(request):
    return render(request, 'user/loginform.html')


def login(request):
    email = request.POST['email']
    password = request.POST['password']

    user = User.objects.filter(email=email).filter(password=password)
    print(user, type(user))
    if not user:
        return HttpResponseRedirect('/user/loginform')
    else:
        return HttpResponseRedirect('/')

