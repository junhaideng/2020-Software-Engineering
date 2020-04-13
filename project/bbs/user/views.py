"""
author: Edgar
实现用户的相关操作
"""
from math import ceil

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from .models import User, ExpData
from django.contrib.auth.models import User as AuthUser
from django.core.paginator import Paginator


@require_http_methods(["GET", "POST"])
def forget(request):
    """忘记密码 author 祁山青"""
    if request.method == "POST":
        username = request.POST.get("username")  # 获取用户名
        flag = User.objects.filter(user__username=username).exists()  # 是否存在该用户名的用户
        if flag:
            u = User.objects.get(user__username=username)
            Question = u.question
            request.session['msg'] = username
            return render(request, 'user/forgetdetail.html', context={"message": None, "question": Question})
        else:
            message = "此用户不存在"
            request.session['user_forget_message'] = message
            return redirect(reverse("user:forget"))
    else:
        message = "请输入用户名"
        if request.session.get("user_forget_message"):
            message = request.session.pop("user_forget_message")
        return render(request, 'user/forget.html', context={"message": message})


@require_http_methods(["GET", "POST"])
def forgetdetail(request):
    """验证密保 author 祁山青
    ToDo: 验证三个密保，两个正确即可重置
    """
    username = request.session.get('msg')
    u = User.objects.get(user__username=username)
    RightAnswer = u.answer
    Question = u.question
    if request.method == "POST":
        answer = request.POST.get("answer")
        if answer == RightAnswer:
            # 重置密码
            user1 = AuthUser.objects.get(username=username)
            user1.set_password('123456')
            user1.save()
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
        return render(request, 'user/forgetdetail.html', context={"message": message, "question": Question})


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
                request.session['username'] = username
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
        return render(request, 'user/login.html', context={"message": message})


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


@login_required()
@require_http_methods(["GET", "POST"])
def file(request):
    """用户上传的文件(实验数据)
    @author： Edgar
    TODO: 分页显示
    """
    if request.method == "POST":  # POST 代表删除文件
        file_id = request.POST.get("id")  # 获取文件的id
        if file_id:
            ExpData.objects.get(id=file_id).delete()  # 删除文件
            return JsonResponse({"status": "success"})  # 删除成功
        return JsonResponse({"status": "failed"})   # 无此id
    else:
        user_id = request.user.id
        files = ExpData.objects.filter(user_id=user_id)  # 获取该用户的所有文件
        per_page_num = 10  # 每一页的帖子数
        p = Paginator(files, per_page_num)  # 分页对象
        total = ceil(files.count() / per_page_num) * 10  # 总共页数， *10 是为了适应在layui中的显示(count变量)
        curr_page = 1  # 默认的时候指定的是第一页
        data = []
        if request.GET.get("page"):  # 如果url中含有参数page，那么指定其页数 (?page=num)
            curr_page = request.GET.get("page")
        page = p.page(curr_page)  # 获取当前页面的信息
        if page:
            for file in page:
                data.append(
                    {"name": file.name, "path": file.path, "downloads": file.download_times, "exp_type": file.exp_type,
                     "date": file.date, "id": file.id})
        return render(request, 'user/file.html', context={"files": data, "total":total, "curr_page":curr_page})


@login_required()
@require_http_methods(["GET", "POST"])
def resetpwd(request):
    """修改密码
    author 祁山青
    """
    if request.method == "POST":
        username = request.session['username']
        u = AuthUser.objects.get(username=username)
        oldpwd = request.POST.get("oldpwd")
        newpwd = request.POST.get("newpwd")
        confirm = request.POST.get("confirm")
        res = authenticate(username=username, password=oldpwd)  # 进行账号密码验证
        if res:
            if confirm != newpwd:
                message = "两次密码不正确"
                # 重置密码
            else:
                u.set_password(newpwd)
                u.save()
                message = "您的密码已经修改"
            return render(request, 'user/resetpwd.html', context={"message": message})
        else:
            message = "旧密码错误"
            request.session['user_reset_message'] = message
            return render(request, 'user/resetpwd.html', context={"message": message})
    else:
        message = None
        if request.session.get('user_reset_message'):
            message = request.session.pop('user_reset_message')
        return render(request, 'user/resetpwd.html', context={"message": message})
