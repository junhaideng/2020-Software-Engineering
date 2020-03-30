"""
author: Edgar
实现用户的相关操作
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from .models import User
from django.contrib.auth.models import User as AuthUser


@require_http_methods(["GET", "POST"])
def login(request):
    """登录处理"""
    if request.method == "POST":
        username = request.POST.get("username")  # 获取表单中的账号密码
        password = request.POST.get("password")
        flag = User.objects.filter(user__username=username).exists()  # 是否存在该用户名的用户
        if flag:
            user = authenticate(username=username, password=password)  # 进行账号密码验证
            if user:  # 登录成功
                auth_login(request, user)
                if request.POST.get("next"):
                    return redirect(request.POST.get("next"))
                return redirect("/")
            else:
                message = "密码错误，请重新输入"
        else:
            message = "不存在此用户"
        request.session['user_login_message'] = message
        return redirect(reverse("user:login"))
    else:
        message = None
        if request.session.get("user_login_message"):
            message = request.session.pop("user_login_message")
        return render(request, 'user/login.html', context={"message":message})


@require_http_methods(["GET", "POST"])
def signup(request):
    """注册处理"""
    if request.method == "POST":
        username = request.POST.get("username")
        if not User.objects.filter(user__username=username):
            password = request.POST.get("password")
            confirm = request.POST.get("confirm")
            if password == confirm:
                email = request.POST.get("email")
                auth = AuthUser(username=username, password=password, email=email)
                auth.set_password(password)
                auth.save()
                User(user=auth).save()
                auth_login(request, auth)
                if request.POST.get("next"):
                    return redirect(request.POST.get("next"))
                return redirect("/")
            else:
                message = "两次密码不正确"
        else:
            message = "已存在该用户名"
        return render(request, 'user/signup.html', context={"message": message})
    else:
        return render(request, 'user/signup.html')


def forget(request):
    """密码寻回"""
    return HttpResponse("forget")


@login_required()
@require_http_methods(["GET"])
def logout(request):
    """用户的登出"""
    auth_logout(request)
    return redirect("/")


@login_required()
def profile(request):
    if request.method == "GET":
        user = request.user
        profile = User.objects.get(user=user).profile
        return render(request, 'user/profile.html', context={"profile": profile})


@login_required()
def history(request):
    return render(request, 'user/history.html')


def file(request):
    return render(request, 'user/file.html')
