from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.db.models import Max, F
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from board.models import Board
from board.myblock import Myblock


# 게시판 리스트
def list(request, page=0):

    boardlist = Board.objects.all().order_by('-groupno', 'orderno')
    page = 1 if page == 0 else page

    # Django내장클래스 Paginator(게시글 리스트, 페이지당 게시물 갯수)
    p = Paginator(boardlist, 1)

    # 페이지 블록 설정 클래스 Myblock(표시페이지갯수, 현재페이지, Paginator객체)
    b = Myblock(5, p.num_pages, page, p)

    data = {
        'boardlist': p.page(page).object_list,  # 현재 페이지 게시물 리스트
        'totalcount': p.count,     # 전체 게시물 갯수
        'nowpage': page,    # 현재페이지
        'b': b,             # 페이지 블록 설정 정보
        'page_startindex': p.page(page).start_index()  # for 게시글 번호 작업
    }

    return render(request, 'board/list.html', data)


# 글 보기
def view(request, page=1, id=0):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/board')
    else:
        # id로 글 가져오기
        board = Board.objects.get(id=id)

        # render로 넘길 context 사전형 객체
        data = {
            'board': board,
            'page': page
        }

        # set_cookie
        response = render(request, 'board/view.html', data)

        if request.COOKIES.get('alreadyseenpost') is not None:
            viewer = request.COOKIES.get('alreadyseenpost')
            viewerlist = viewer.split('+')

            # id 없을 경우 조회수 업데이트 & id 쿠키에 넣어주기
            if str(id) not in viewerlist:
                Board.objects.filter(id=id).update(hit=F('hit')+1)
                viewer = viewer + str(id) + '+'
        else:
            viewer = str(id) + '+'

        # 만료시간 (오늘 자정까지)
        tomorrow = datetime.today()+timedelta(days=1)
        tomorrow = datetime.replace(tomorrow, hour=0, minute=0, second=0)
        response.set_cookie('alreadyseenpost', viewer, expires=tomorrow)

        return response


# 글삭제
def delete(id=0):
    Board.objects.filter(id=id).update(delete=1)
    return HttpResponseRedirect('/board')


# 글작성
def write(request):
    board = Board()

    board.title = request.POST['title']
    board.content = request.POST['content']
    max = Board.objects.aggregate(max_groupno=Max('groupno'))
    board.groupno = (0 if max['max_groupno'] is None else max['max_groupno']) + 1
    board.user_id = request.session['authuser']['id']

    board.save()

    return HttpResponseRedirect('/board')


# 글작성 폼 이동
def writeform(request):
    if 'authuser' not in request.session:
        return HttpResponseRedirect('/board')
    else:
        return render(request, 'board/write.html')


# 글수정 폼 이동
def modifyform(request, id=0):
    board = Board.objects.get(id=id)
    data = {'board': board}
    return render(request, 'board/modify.html', data)


# 글수정
def modify(request, id=0):
    board = Board.objects.get(id=id)

    board.title = request.POST['title']
    board.content = request.POST['content']

    board.save()

    return HttpResponseRedirect('/board')


# 답글쓰기 폼 이동
def writereplyform(request, id=0):
    return HttpResponseRedirect(f'/board/writeform?id={id}')


# 답글쓰기
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
