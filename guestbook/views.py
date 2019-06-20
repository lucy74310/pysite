from django.http import HttpResponseRedirect
from django.shortcuts import render
from guestbook.models import Guestbook


# Create your views here.
def list(request):
    guestbooklist=Guestbook.objects.all().order_by('-id')
    data={'guestbooklist':guestbooklist}

    return render(request, 'guestbook/list.html', data)


def write(request):
    guestbook=Guestbook()

    guestbook.name=request.POST['name']
    guestbook.password=request.POST['password']
    guestbook.content=request.POST['content']

    guestbook.save()

    return HttpResponseRedirect('/guestbook')


def deleteform(request, id=0):
    data={'id':id}
    return render(request, 'guestbook/deleteform.html', data)


def delete(request, id=0):
    password=request.POST['password']
    guestbook=Guestbook.objects.filter(id=id).filter(password=password)
    guestbook.delete()
    return HttpResponseRedirect('/guestbook')