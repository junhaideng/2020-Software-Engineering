"""
author: Edgar
实现用户的相关操作
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from .models import User
from django.contrib.auth.models import User as AuthUser

@require_http_methods(["GET", "POST"])
def forget(request):
    """忘记密码 author 祁山青"""
    if request.method == "POST":
        username = request.POST.get("username")  # 获取用户名
        flag = User.objects.filter(user__username=username).exists()  # 是否存在该用户名的用户
        if flag:
            u = User.objects.get(user__username=username)
            Question = u.question
            request.session['msg']=username
            return render(request, 'user/forgetdetail.html', context={"message":None,"question":Question})
        else:
            message = "此用户不存在"
            request.session['user_forget_message'] = message
            return redirect(reverse("user:forget"))
    else:
        message = "请输入用户名"
        if request.session.get("user_forget_message"):
            message = request.session.pop("user_forget_message")
        return render(request, 'user/forget.html', context={"message":message})

@require_http_methods(["GET", "POST"])
def forgetdetail(request):
    """验证密保 author 祁山青
    ToDo: 验证三个密保，两个正确即可重置
    """
    username=request.session.get('msg')
    u=User.objects.get(user__username=username)
    RightAnswer=u.answer
    Question=u.question
    if request.method == "POST":
        answer = request.POST.get("answer")
        if answer==RightAnswer:
            #重置密码
            user1 = AuthUser.objects.get(username=username)
            user1.set_password('123456')
            message = "您的密码已经重置为:123456 请返回主页重新登陆"
            return render(request, 'user/forgetdetail.html', context={"message": message, "question": Question})
        else:
            message = "答案错误"
            request.session['user_answer_message'] = message
            return render(request, 'user/forgetdetail.html', context={"message": message, "question": Question})
    else:
        message = None
        if request.session.get('user_answer_message'):
            message = request.session.pop('user_answer_message')
        return render(request, 'user/forgetdetail.html', context={"message":message,"question":Question})

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
                user1 = User(user=auth)
                user1.question = request.POST.get("passwordquestion")
                user1.answer = request.POST.get("passwordanswer")
                user1.save()
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
