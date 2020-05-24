"""
author: Edgar
对搜索界面的显示进行处理
"""
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from course.models import Course
from user.models import Files, User
from post.models import Post
from course.models import TeacherOfCourse


def search(request):
    """搜索相关"""
    if request.method == 'POST':  # 处理ajax对应的事件，可以实时的获取信息
        value = request.POST.get("value")
        type = request.POST.get("type")
        data = []
        if value and type == "course":
            courses = Course.objects.filter(name__contains=value)  # 查询
            for course in courses:
                data.append({"name": course.name, "id": course.id})
        if value and type == "post":
            posts = Post.objects.filter(topic__contains=value)
            for post in posts:
                data.append({"name": post.topic, "id": post.id, "content": post.content})
        return JsonResponse({"data": data})  # 返回数据，前端处理显示
    if request.method == "GET":  #
        keyword = request.GET.get("keyword")
        if keyword:  # 如果含有keyword处理 点击search按钮之后的事件
            data = None
            return render(request, 'search/search.html', context={"keyword": keyword, "data": data})
        return redirect(reverse("home:index"))  # 否则只是简单的访问该网页


def search_course(request):
    """搜索课程"""
    keyword = request.GET.get("keyword")
    courses = Course.objects.filter(name__contains=keyword)  # 查询
    data = []
    for course in courses:
        TeacherOfCourse.objects.filter(course_id=course.id)
        data.append(
            {"name": course.name, "id": course.id, "teacher": TeacherOfCourse.objects.get(course_id=course.id).name})
    return render(request, 'search/search.html', context={"keyword": keyword, "data": data})


def search_post(request):
    """搜索帖子"""
    keyword = request.GET.get("keyword")
    posts = Post.objects.filter(topic__contains=keyword)  # 获取所有满足条件的帖子
    data = []
    for post in posts:
        content = post.content
        if len(content) > 20:
            content = content[:20] + "..."  # 对内容处理一下
        data.append({"topic": post.topic, "content": content, "id": post.id, "time": post.created_time})
    return render(request, 'search/search_post.html', context={"keyword": keyword, "data": data})


@csrf_exempt
def files(request):
    """下载页的文件显示"""
    if request.method == "GET":
        files = Files.objects.all()  # 如果是get请求的话，会将所有的文件都进行显示
        return render(request, "download/index.html", context={"files": files})
    elif request.method == "POST":  # 异步请求返回json数据，前端进行处理
        value = request.POST.get("value")
        # 将文件的一系列信息进行返回
        files = list(map(lambda x: {"name": x.name, "type": x.type, "date": str(x.date).split(" ")[0],
                                    "download_times": x.download_times, "url": x.path,
                                    "username": User.objects.get(user_id=x.user_id).user.username},
                         Files.objects.filter(Q(type__contains=value) | Q(name__contains=value))))
        return JsonResponse({"data": files})
