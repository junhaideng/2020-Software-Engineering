"""
author: Edgar
课程路由下的页面显示
TODO: 如何显示课程，怎么样显示
"""
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Course,TeacherOfCourse,CourseDes,Major
from user.models import ExpData
import time
import os
import json

TYPES = (  # 课程的类型
    ("CO", "必修"),  # 必修
    ("El", "选修"),  # 选修
    ("Ex", '实验'),  # 实验
    ("Ot", '其他')  # 其他
)

SCHOOLS=(   #   学院名称
    ("1","电子信息与电气工程学院"),
    ("2","机械与动力工程学院"),
    ("3","船舶海洋与建筑工程学院"),
    ("4","生物医学工程学院"),
    ("5","航空航天学院"),
    ("6","数学科学院"),
    ("7","物理与天文学院"),
    ("8","化学化工学院"),
    ("9","致远学院"),
    ("10","医学院"),
    ("11","安泰经济与管理学院"),
    ("12","人文学院"),
)

@require_http_methods(["GET","POST"])
def index(request):
    """课程界面的首页"""
    #啥都不干
    return render(request, 'course/index.html')


@require_http_methods(["POST"])
def upload(request):
    if request.method == "POST":
        file = request.FILES.get("file")
        exp_type = request.POST.get("type")
        pre_path = os.path.join(os.path.join(settings.BASE_DIR, "media"), "experiment_data/")
        alias = time.strftime("%Y_%m_%d_%H_%M_%S_", time.localtime()) + file.name
        if not os.path.exists(pre_path):
            os.mkdir(pre_path)
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


@require_http_methods(["GET","POST"])
def details(request,type,school):
    """课程界面的首页"""
    class Newcourse(): #建立一个新的类
        def __init__(self):
            self.pk= None #课程主键
            self.name = '无'  # 课程的名字
            self.school ='无'  # 专业名
            self.teacher= [] #老师 可能有多个
    if 1:
        Type=type
        School= school
        if Type=="0":#我将没有选择的时候设置为了0
            courselist=Course.objects.filter(school=School)
        elif School=="0":
            courselist = Course.objects.filter(type=Type)
        else:
            courselist = Course.objects.filter(school=School,type=Type)
        List=[]
        for course in courselist:#将教师和课程 组合在一个列表中
            a=Newcourse()
            a.name=course.name
            a.pk=course.pk
            a.school=SCHOOLS[int(course.school)-1][1]
            info=TeacherOfCourse.objects.filter(course_id=course.pk)
            if info.count()==0:
                a.teacher=['None']
            else:
                for b in TeacherOfCourse.objects.filter(course_id=course.pk):
                    a.teacher.append(b.name)
            List.append(a)
        return render(request, 'course/details.html', {"list": List})

@require_http_methods(["GET","POST"])
def coursedes(request,pk):
    course=Course.objects.get(pk=pk)
    teachers=TeacherOfCourse.objects.filter(course_id=course.pk)
    flag=1
    if teachers.count()==0:
        flag=0
    des = CourseDes.objects.get(course_id=course.pk)
    for i in TYPES:
        if i[0]==course.type:
            type=i[1]
    school=SCHOOLS[int(course.school)-1][1]
    return render(request,'course/coursedes.html',{"course":course,"teacherList":teachers,"des":des,"school":school,"type":type,"flag":flag})