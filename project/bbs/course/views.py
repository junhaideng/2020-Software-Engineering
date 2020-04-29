"""
author: Edgar
课程路由下的页面显示
TODO: 如何显示课程，怎么样显示
"""
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Course,TeacherOfCourse,CourseDes,Major
from user.models import ExpData
import time
import os


def index(request):
    """课程界面的首页"""
    return render(request, 'course/index.html')


@require_http_methods(["POST"])
def upload(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        exp_type = request.POST.get("type")
        pre_path = os.path.join(os.path.join(settings.BASE_DIR, "media"), "experiment_data/")
        alias = time.strftime("%Y_%m_%d_%H_%M_%S_", time.localtime()) + file.name
        path = pre_path + alias
        with open(path, "wb") as f:
            for chuck in file.chunks():
                f.write(chuck)
        ExpData.objects.create(user_id=request.user.id,
                               exp_type=exp_type,
                               download_times=0,
                               path="/media/experiment_data/"+alias,
                               name=os.path.splitext(file.name)[0]).save()
        return JsonResponse({"status": "success"})

@require_http_methods(["GET", "POST"])
def details(request):
    class Newcourse:
        def __init__(self):
            self.name = 0  # 课程的名字
            self.major =1  # 专业名
            self.teacher= []

    message = None
    if request.method =="POST":
        Type=request.POST.get("type")
        courselist=Course.objects.filter(type=Type)
        List=[]
        for course in courselist:
            a=Newcourse()
            a.name=course.name
            a.major=course.major
            if TeacherOfCourse.objects.filter(course_id=course.pk)==0:
                a.teacher=['None']
            else:
                for b in TeacherOfCourse.objects.filter(course_id=course.pk):
                    a.teacher.append(b.name)
            List.append(a)
        message = '搜索结果如上'
        return render(request, 'course/details.html', {"message": message,"List":List})
    else:
        message='暂无搜索结果'
        return render(request, 'course/details.html', {"message":message})

