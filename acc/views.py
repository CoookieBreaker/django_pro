from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib import messages

# Create your views here.
def update(request):
    if request.method == "POST":
        u = request.user
        pw = request.POST.get("upass")
        co = request.POST.get("comment")
        pi = request.FILES.get("pic")
        if pw:
            u.set_password(pw)
        if pi:
            u.pic.delete() # 수정하기 전에 기존의 사진을 먼저 삭제한다.
            u.pic = pi
        u.comment = co
        u.save()
        login(request, u)
        messages.error(request, "정보가 변경되었습니다.")
        return redirect("acc:profile")
    return render(request, "acc/update.html")

def delete(request):
    if check_password(request.POST.get("passcheck"),request.user.password):
        request.user.pic.delete() # 계정이 삭제되기 전에 사진을 먼저 삭제
        request.user.delete()
    else:
        messages.error(request, "정보 일치하지 않습니다. ")
    return redirect("acc:index")

def profile(request):
    return render(request, "acc/profile.html")

def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        ag = request.POST.get("uage")
        co = request.POST.get("ucom")
        im = request.FILES.get("uimg")
        User.objects.create_user(username = un, password = pw, age = ag, comment = co, pic = im)
        return redirect("acc:login")
    return render(request, "acc/signup.html")

def index(request):
    return render(request, "acc/index.html")

def login_user(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        pw = request.POST.get("upass")
        user = authenticate(username=un, password=pw)
        if user:
            login(request, user)
            messages.success(request,f"{user} 님 환영합니다.")
            return redirect("acc:index")
        else: # 로그인 실패했어요~~ (19일차에 할거)
            messages.error(request,"아이디나 패스워드가 잘못되었습니다 :(")
    return render(request, "acc/login.html")

def logout_user(request):
    logout(request)
    return redirect("acc:index")