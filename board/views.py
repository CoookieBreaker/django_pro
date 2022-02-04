from this import d
from django.shortcuts import render, redirect
from acc.models import User
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages
# Create your views here.

def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect('board:detail', bpk)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect('board:detail', bpk)

def delply(request,bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
    else:
        pass
    return redirect("board:detail", bpk)

def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    c = request.POST.get("com")
    Reply(b=b, replyer=request.user,comment=c,pubdate=timezone.now()).save()
    return redirect("board:detail", bpk)

def update(request, bpk):
    b = Board.objects.get(id=bpk)
    #다른 사람이 악의적으로 접근할때
    if request.user != b.writer:
        messages.error(request, "수정권한이 없습니다.")
        return redirect("board:index")
    if request.method == "POST":
        b.subject = request.POST.get("subject")
        b.content = request.POST.get("content")
        b.save()
        return redirect("board:detail", bpk)
    context = {
        "b" : b
    }
    return render(request, "board/update.html", context)

def create(request):
    if request.method == "POST":
        su = request.POST.get("subject")
        co = request.POST.get("content")
        Board(subject = su, writer = request.user, content = co, pubdate = timezone.now()).save()
        return redirect("board:index")
    return render(request, "board/create.html")

def delete(request, bpk):
    b = Reply.objects.get(id=bpk)
    if b.writer == request.user:
        b.delete()
    else:
        messages.error(request, "삭제권한이 없습니다.") # 19일차 메세지 띄어줌!!
    return redirect("board:index")

def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        "b" : b,
        "rlist" : r
    }
    return render(request, "board/detail.html", context)

def index(request):
    pg = request.GET.get("page", 1)
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw", "")
    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw) # 언더바 두개인거 주의하기!!
        elif cate == "wri":
            from acc.models import User
            try:
                u = User.objects.get(username=kw) # 레코드는 레코드끼리 비교해야 트루가 나온다.
                b = Board.objects.filter(writer=u) # 이것만 입력했을경우 레코드랑 문자열을 비교하게된다.
                # writer는 models에 있는 레코드이며 kw는 문자열이다.
            except:
                b = Board.objects.none()
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
    else:
        b = Board.objects.all()

    pag = Paginator(b, 10)
    obj = pag.get_page(pg)
    context = {
        "blist" : obj,
        "cate" : cate,
        "kw" : kw
    }
    return render(request, "board/index.html", context)