from math import ceil

from django.core.paginator import Paginator
from django.db.models import Max, F
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from board.models import Board


def list(request, page=0):
    boardlist = Board.objects.all().order_by('-groupno', 'orderno')

    page = 1 if page == 0 else page

    p = Paginator(boardlist, 2)

    pagenum_perblock = 4
    blocknums = ceil(float(p.num_pages) / pagenum_perblock)
    currentblock = ceil(float(page) / pagenum_perblock)
    blockstartpage = ((currentblock-1) * pagenum_perblock) + 1
    blockendpage = p.num_pages if blocknums == currentblock else (blockstartpage + (pagenum_perblock-1))

    blockinfo = {
        'pagenum_perblock': pagenum_perblock,
        'blocknums': blocknums,
        'currentblock': currentblock,
        'range': range(blockstartpage, blockendpage+1),
        'blockstartpage': blockstartpage,
        'blockendpage': blockendpage,
        'hasprevious': p.page(blockstartpage).has_previous(),
        'hasnext': p.page(blockendpage).has_next(),
        'startindex': p.page(page).start_index()
    }

    data = {
        'boardlist': p.page(page).object_list,
        'paginator': p,
        'nowpage': page,
        'b': blockinfo
    }

    return render(request, 'board/list.html', data)


def view(request, id=0):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/board')
    else:
        Board.objects.filter(id=id).update(hit=F('hit')+1)
        board = Board.objects.get(id=id)

        data = {'board': board}
        return render(request, 'board/view.html', data)


def delete(request, id=0):
    Board.objects.filter(id=id).update(delete=1)
    return HttpResponseRedirect('/board')


def write(request):
    board = Board()

    board.title = request.POST['title']
    board.content = request.POST['content']
    max = Board.objects.aggregate(max_groupno=Max('groupno'))
    board.groupno = (0 if max['max_groupno'] is None else max['max_groupno']) + 1
    board.user_id = request.session['authuser']['id']

    board.save()

    return HttpResponseRedirect('/board')


def writeform(request):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/board')
    else:
        return render(request, 'board/write.html')


def modifyform(request, id=0):
    board = Board.objects.get(id=id)
    data = {'board': board}
    return render(request, 'board/modify.html', data)


def modify(request, id=0):
    board = Board.objects.get(id=id)

    board.title = request.POST['title']
    board.content = request.POST['content']

    board.save()

    return HttpResponseRedirect('/board')


def writereplyform(request, id=0):
    return HttpResponseRedirect(f'/board/writeform?id={id}')


def writereply(request):
    parentboard = Board.objects.get(id=request.POST['id'])

    print(parentboard.id)

    board = Board()

    board.title = request.POST['title']
    board.content = request.POST['content']
    board.groupno = parentboard.groupno
    board.orderno = parentboard.orderno + 1

    Board.objects.filter(groupno=board.groupno). \
        filter(orderno__gte=board.orderno). \
        update(orderno=F('orderno')+1)

    board.depth = parentboard.depth + 1
    board.user_id = request.session['authuser']['id']

    board.save()

    return HttpResponseRedirect(f'/board')
