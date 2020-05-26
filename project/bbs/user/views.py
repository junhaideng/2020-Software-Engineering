"""
author: Edgar
实现用户的相关操作
"""
from math import ceil
import os
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from .models import User, Files
from django.contrib.auth.models import User as AuthUser
from django.core.paginator import Paginator
from django.conf import settings
import time
from post.models import Post, PostReply, PostComment
import operator


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
    """
    登录处理
    @author: Edgar
    """
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
    """
    注册处理
    @author: Edgar
    """
    if request.method == "POST":
        username = request.POST.get("username")
        if not User.objects.filter(user__username=username):
            password = request.POST.get("password")
            confirm = request.POST.get("confirm")
            if password == confirm:
                email = request.POST.get("email")
                auth = AuthUser(username=username, email=email)
                auth.set_password(password)
                auth.save()
                user1 = User(user=auth)
                user1.save()
                request.session['username'] = username
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
    """
    用户的登出
    @author: Edgar
    """
    auth_logout(request)
    return redirect("/")


@login_required()
def profile(request):
    """
        个人资料显示
        @author: Edgar，吴嘉锐
    """
    if request.method == "GET":
        user = request.user
        profile = User.objects.get(user=user).profile
        user_name = User.objects.get(user=user).user
        sex = "女"  # 把sex性别转换成文字，不太会用高级语句。。
        if User.objects.get(user=user).sex:
            sex = '男'
        elif User.objects.get(user=user).sex is None:
            sex = '保密'
        if User.objects.get(user=user).academy is None:
            academy = '您还没有设置学院哦！'
        else:
            academy = User.objects.get(user=user).academy
        grade_index = {'FR': '大一', 'SO': '大二', 'JR': '大三', 'SR': '大四', "OT": '其他', "UN": "未知"}
        grade = grade_index[User.objects.get(user=user).grade]
        return render(request, 'user/profile.html', context={"profile": profile, "username": user_name, "sex": sex,
                                                             "academy": academy, "grade": grade})


@login_required()
@require_http_methods(["GET", "POST"])
def modify(request):
    """
        个人资料的修改
        @author: 吴嘉锐
    """
    user = request.user
    if request.method == "POST":
        sex_index = {'男': True, '女': False, '保密': None}  # 性别、年级的字典
        grade_index = {'大一': 'FR', '大二': 'SO', '大三': 'JR', '大四': 'SR', "其他": 'OT', "未知": "UN"}

        user_c = User.objects.get(user=user)  # 储存需要修改的数据

        user_c.user.username = request.POST.get("nickname")  # 获得用户的修改值
        if request.POST.get("college") != '不修改':
            user_c.academy = request.POST.get("college")
        if request.POST.get("sex") != '不修改':
            user_c.sex = sex_index[request.POST.get("sex")]
        if request.POST.get("grade") != '不修改':
            user_c.grade = grade_index[request.POST.get("grade")]

        if request.FILES.get("profile_c") is not None:
            img = request.FILES.get("profile_c")
            media = settings.MEDIA_ROOT
            with open(media + '/profile/' + request.POST.get("nickname") + '.jpg', 'wb') as save_img:
                for part in img.chunks():
                    save_img.write(part)
                    save_img.flush()
            user_c.profile = '/media/profile/' + request.POST.get("nickname") + '.jpg'

        user_c.user.save()
        user_c.save()
        return HttpResponseRedirect('/user/profile')
    else:
        user_name = User.objects.get(user=user).user
        if User.objects.get(user=user).sex:
            sex = '男'
        elif not User.objects.get(user=user).sex:
            sex = '女'
        else:
            sex = '保密'
        college = User.objects.get(user=user).academy
        grade_index = {'FR': '大一', 'SO': '大二', 'JR': '大三', 'SR': '大四', "OT": '其他', "UN": "未知"}
        grade = grade_index[User.objects.get(user=user).grade]

        return render(request, 'user/modify.html',
                      {'username': user_name, 'sex': sex, 'college': college, 'grade': grade})


@login_required()
def history(request):
    """
            发帖记录
            @author: 吴嘉锐  搬运了Edgar的分页语句
    """
    post_histories = Post.objects.filter(author_user_id=request.user.id)  # 发帖的记录
    if post_histories.exists():
        per_page_num = 10  # 每一页的记录数
        p = Paginator(post_histories, per_page_num)  # 分页对象
        total = ceil(post_histories.count() / per_page_num) * 10  # 总共页数， *10 是为了适应在layui中的显示(count变量)
        curr_page = 1  # 默认的时候指定的是第一页
        data = []
        if request.GET.get("page"):  # 如果url中含有参数page，那么指定其页数 (?page=num)
            curr_page = request.GET.get("page")
        page = p.page(curr_page)  # 获取当前页面的信息
        if page:
            for post in page:
                if len(post.content) < 10:
                    content = post.content
                else:
                    content = post.content[0:8] + '...'
                data.append(
                    {"topic": post.topic, "created_time": post.created_time, "content": content}
                )
        else:
            data = None
            total = 0
            curr_page = 1
    else:
        data = None
        total = 0
        curr_page = 1
    return render(request, 'user/history.html',
                  context={"post_histories": data, "total": total, "curr_page": curr_page})


@login_required()
@require_http_methods(["GET", "POST"])
def file(request):
    """
    用户上传的文件
    @author： Edgar
    """
    if request.method == "POST":  # POST 代表删除文件
        file_id = request.POST.get("id")  # 获取文件的id
        if file_id:
            f = Files.objects.get(id=file_id)  # 先获取该文件
            os.remove(settings.BASE_DIR + f.path)
            f.delete()

            return JsonResponse({"status": "success"})  # 删除成功
        return JsonResponse({"status": "failed"})  # 无此id
    else:
        user_id = request.user.id
        files = Files.objects.filter(user_id=user_id)  # 获取该用户的所有文件
        if files.exists():
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
                        {"name": file.name, "path": file.path, "downloads": file.download_times,
                         "type": file.type,
                         "date": file.date, "id": file.id})
        else:
            data = None
            total = 0
            curr_page = 1
        return render(request, 'user/file.html', context={"files": data, "total": total, "curr_page": curr_page})


@login_required()
@require_http_methods(["GET", "POST"])
def resetpwd(request):
    """修改密码
    author 祁山青
    """
    if request.method == "POST":
        username = request.session.get('username')
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
            return redirect(reverse("user:login"))
        else:
            message = "旧密码错误"
            request.session['user_reset_message'] = message
            return render(request, 'user/resetpwd.html', context={"message": message})
    else:
        message = None
        if request.session.get('user_reset_message'):
            message = request.session.pop('user_reset_message')
        return render(request, 'user/resetpwd.html', context={"message": message})


@login_required()
@require_http_methods(["GET", "POST"])
def setquestion(request):
    """设置密保
        author 祁山青
        """
    username = request.session.get('username')
    U = User.objects.get(user__username=username)
    if U.question is None:  # 原先没有密保 则需要输入密码设置密保
        flag = 0
    else:  # 原先无密保 则需要验证原先密保更改密保
        flag = 1
    if request.method == "POST" and flag == 0:  # 原先无密保
        pwd = request.POST.get("pwd")  # pwd是前端post传来的密码
        res = authenticate(username=username, password=pwd)  # 进行账号密码验证
        if res:
            question = request.POST.get("newQuestion")  # 同 pwd
            answer = request.POST.get("newAnswer")  # 同 pwd
            U.question = question  # 修改用户的密保问题
            U.answer = answer
            U.save()  # 存储用户
            message = "密保设置成功！"
            return render(request, 'user/setquestion.html',
                          {"message": message, "flag": flag})  # 返回给user/setquestion.html
        # "message" 是html里面id 为message的对象 "flag"同理，这里的具体传递方法为{“html中的Id”,值}
        else:
            message = "密码错误"
            request.session['user_setquestion_message'] = message
            return render(request, 'user/setquestion.html', {"message": message, "flag": flag})
    elif request.method == "POST" and flag == 1:  # 有原来的密保
        oldanswer = request.POST.get("oldAnswer")
        newanswer = request.POST.get("newAnswer")
        newquestion = request.POST.get("newQuestion")
        if oldanswer == U.answer:
            U.question = newquestion
            U.answer = newanswer
            U.save()
            message = "密保设置成功！"
            return render(request, 'user/setquestion.html',
                          {"message": message, "flag": flag, "oldQuestion": U.question})
        else:
            message = "旧密保回答错误"
            request.session['user_setquestion_message'] = message
            return render(request, 'user/setquestion.html',
                          {"message": message, "flag": flag, "oldQuestion": U.question})
    else:
        message = None
        if request.session.get('user_setquestion_message'):
            message = request.session.pop('user_setquestion_message')
        return render(request, 'user/setquestion.html', {"message": message, "flag": flag, "oldQuestion": U.question})


@login_required()
@require_http_methods(["POST", "GET"])
def upload(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        type = request.POST.get("type")
        desc = request.POST.get("desc")
        pre_path = os.path.join(os.path.join(settings.BASE_DIR, "media"), "files/")
        alias = time.strftime("%Y_%m_%d_%H_%M_%S_", time.localtime()) + file.name
        if not os.path.exists(pre_path):
            os.mkdir(pre_path)
        path = pre_path + alias
        with open(path, "wb") as f:
            for chuck in file.chunks():
                f.write(chuck)
        Files.objects.create(user_id=request.user.id,
                             type=type,
                             download_times=0,
                             path="/media/files/" + alias,
                             name=os.path.splitext(file.name)[0],
                             desc=desc).save()
        return JsonResponse({"status": "success"})
    else:
        return render(request, 'user/upload.html')


@login_required()
@require_http_methods(["GET"])
def notice(request):
    """
        回复通知
        author 吴嘉锐
    """
    my_post = Post.objects.filter(author_user_id=request.user.id)  # 用户发的贴子
    my_reply = PostReply.objects.filter(post_user_id=request.user.id)  # 用户的回复
    notice_unread = []  # 未读消息
    notice_read = []  # 已读消息

    received_reply = []  # 获得用户收到的回复
    for post in my_post:
        reply_to_post = PostReply.objects.filter(post_id=post.id)
        for each_reply in reply_to_post:
            received_reply.append(each_reply)
            if User.objects.filter(id=each_reply.post_user_id) is not None:
                username = User.objects.get(id=each_reply.post_user_id).user.username
            else:
                username = '该用户已注销'
            if not each_reply.if_read:
                each_reply.if_read = True
                each_reply.save()
                notice_unread.append(
                    {"user": username, "content": each_reply.content,
                     "mytext": post.topic, "time": each_reply.created_date}
                )
            else:
                notice_read.append(
                    {"user": username, "content": each_reply.content,
                     "mytext": post.topic, "time": each_reply.created_date}
                )

    received_comment = []  # 获得用户收到的评论
    for reply in my_reply:
        comment_to_reply = PostComment.objects.filter(reply=reply.id)
        for each_comment in comment_to_reply:
            received_comment.append(each_comment)
            if User.objects.filter(id=each_comment.post_user_id) is not None:
                username = User.objects.get(id=each_comment.post_user_id).user.username
            else:
                username = '该用户已注销'
            if not each_comment.if_read:
                each_comment.if_read = True
                each_comment.save()
                notice_unread.append(
                    {"user": username,
                     "content": each_comment.content, "mytext": reply.content, "time": each_comment.created_date}
                )
            else:
                notice_read.append(
                    {"user": username,
                     "content": each_comment.content, "mytext": reply.content, "time": each_comment.created_date}
                )

    notice_unread = sorted(notice_unread, key=operator.itemgetter("time"), reverse=True)  # 对时间进行排序
    notice_read = sorted(notice_read, key=operator.itemgetter("time"), reverse=True)

    return render(request, 'user/notice.html', context={"notice_unread": notice_unread, "notice_read": notice_read})
