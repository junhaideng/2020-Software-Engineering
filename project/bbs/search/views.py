"""
author: Edgar
对搜索界面的显示进行处理
"""
from math import ceil

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from course.models import Course
from user.models import Files, User
from post.models import Post
from course.models import TeacherOfCourse
import re


def search(request):
    """搜索相关"""
    # if request.method == 'POST':  # 处理ajax对应的事件，可以实时的获取信息
    #     value = request.POST.get("value")
    #     type = request.POST.get("type")
    #     data = []
    #     if value and type == "course":
    #         courses = Course.objects.filter(name__contains=value)  # 查询
    #         for course in courses:
    #             data.append({"name": course.name, "id": course.id})
    #     if value and type == "post":
    #         posts = Post.objects.filter(topic__contains=value)
    #         for post in posts:
    #             data.append({"name": post.topic, "id": post.id, "content": post.content})
    #     return JsonResponse({"data": data})  # 返回数据，前端处理显示
    if request.method == "GET":  #
        keyword = request.GET.get("keyword")
        if keyword:  # 如果含有keyword处理 点击search按钮之后的事件
            data = None
            return render(request, 'search/search.html', context={"keyword": keyword, "data": data})
        return redirect(reverse("home:index"))  # 否则只是简单的访问该网页


def search_course(request):
    """搜索课程"""
    keyword = request.GET.get("keyword")
    print(keyword)
    courses = Course.objects.filter(name__contains=keyword)  # 查询
    data = []
    per_page_num = 10  # 每一页的数量
    p = Paginator(courses, per_page_num)  # 分页对象
    total = ceil(courses.count() / per_page_num) * 10  # 总共页数， *10 是为了适应在layui中的显示(count变量)
    curr_page = 1 if not request.GET.get("page") else request.GET.get("page")  # 默认的时候指定的是第一页

    for course in p.page(curr_page):
        print(course, course.id, course.school, )
        # 查询到所有对应的老师，这里只显示两个
        teacher_list = list(
            map(lambda x: x.get("name"), TeacherOfCourse.objects.filter(course_id=course.id).values("name")))
        teachers = " ".join(teacher_list[:2]) + " 等" if len(teacher_list) > 2 else " ".join(teacher_list)
        data.append(
            {"name": course.name, "id": course.id, "school": course.school, "teacher": teachers})
    return render(request, 'search/search.html',
                  context={"keyword": keyword, "data": data, "total": total, "curr_page": curr_page})


def search_post(request):
    """搜索帖子"""
    keyword = request.GET.get("keyword")
    posts = Post.objects.filter(topic__contains=keyword)  # 获取所有满足条件的帖子
    per_page_num = 10  # 每一页的帖子数
    p = Paginator(posts, per_page_num)  # 分页对象
    total = ceil(posts.count() / per_page_num) * 10  # 总共页数， *10 是为了适应在layui中的显示(count变量)
    curr_page = 1 if not request.GET.get("page") else request.GET.get("page")  # 默认的时候指定的是第一页
    data = []
    pattern = re.compile("<.*?>(.*?)</.*?>")
    for post in p.page(curr_page):
        content = re.sub(pattern, lambda x: x.group(1) if pattern.match(post.content) else post.content, post.content)
        if len(content) > 20:
            content = content[:20] + "..."  # 对内容处理一下
        data.append(
            {"topic": post.topic, "course": post.course, "content": content, "id": post.id, "time": post.created_time})
    return render(request, 'search/search_post.html',
                  context={"keyword": keyword, "data": data, "total": total, "curr_page": curr_page})


@csrf_exempt
def files(request):
    """下载页的文件显示"""
    if request.method == "GET":
        files = Files.objects.all().order_by("-date")  # 如果是get请求的话，会将所有的文件都进行显示
        per_page_num = 10  # 每一页的数量
        p = Paginator(files, per_page_num)  # 分页对象
        total = ceil(files.count() / per_page_num) * 10  # 总共页数， *10 是为了适应在layui中的显示(count变量)
        curr_page = 1 if not request.GET.get("page") else request.GET.get("page")  # 默认的时候指定的是第一页
        return render(request, "download/index.html",
                      context={"files": p.page(curr_page), "total": total, "curr_page": curr_page})
    elif request.method == "POST":  # 异步请求返回json数据，前端进行处理
        value = request.POST.get("value")
        # 将文件的一系列信息进行返回
        files = list(map(lambda x: {"name": x.name, "type": x.type, "date": str(x.date).split(" ")[0],
                                    "download_times": x.download_times, "url": x.path,
                                    "username": User.objects.get(user_id=x.user_id).user.username},
                         Files.objects.filter(Q(type__contains=value) | Q(name__contains=value))))
        return JsonResponse({"data": files})
