"""
author: Edgar
课程路由下的页面显示
TODO: 如何显示课程，怎么样显示
"""
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Course,TeacherOfCourse,CourseDes,Major,CourseCom
from user.models import ExpData
from user.models import User
import time
import os
from django.contrib.auth.models import User as AuthUser
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
    ("13","材料科学与工程学院"),
    ("14","海洋学院"),
    ("15","药学院"),
    ("16","生命科学技术学院"),
    ("17","农业与生物学院"),
    ("18","凯原法学院"),
    ("19","外国语学院"),
    ("20","体育系"),
    ("21","马克思主义学院"),
    ("22","国际公共与事务学院"),
    ("23","上海高级金融学院")
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
def details(request,type,school,page_num):
    """课程界面的首页"""
    class Newcourse(): #建立一个新的类
        def __init__(self):
            self.pk= None #课程主键
            self.name = '无'  # 课程的名字
            self.school ='无'  # 专业名
            self.teacher= [] #老师 可能有多个
    page_now=page_num#当前页码
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
    p = Paginator(List, 2)
    total_num=p.num_pages #页数
    pagesNum=[]#页码列表
    i=1
    while i <= total_num:
        pagesNum.append(i)
        i = i + 1
    page=p.page(page_num) #对应分页
    pre_page=page_now-1
    if pre_page==0:
        pre_page=1
    next_page=page_now+1
    if next_page==total_num:
        next_page=1
    return render(request, 'course/details.html', {"list": page,"pagesNum":pagesNum,"total_num":total_num,
                                                   "now_page":page_now,"pre_page":pre_page,"next_page":next_page})

@require_http_methods(["GET","POST"])
def coursedes(request,pk):
    class Newcomments():  # 建立一个新的类
        def __init__(self):
            self.image_path = 0  # 头像路径
            self.user_name = '无'  # 用户名字
            self.com = '无'  # 评论
            self.date='None' #评论日期
    course=Course.objects.get(pk=pk)
    teachers=TeacherOfCourse.objects.filter(course_id=course.pk)
    flag=1
    if teachers.count()==0:
        flag=0
    if (CourseDes.objects.filter(course_id=course.pk)).count() == 0:
        des='暂无描述'
    else:
        des = CourseDes.objects.get(course_id=course.pk)
    for i in TYPES:
        if i[0]==course.type:
            type=i[1]
    school=SCHOOLS[int(course.school)-1][1]
    #返回用户评论
    comments=CourseCom.objects.filter(courseid=course.pk)
    new_comments=[]       #返回给前端的列表
    for a in comments:
        name=a.user_name
        u=User.objects.get(user__username=name)
        image_path=u.profile
        if image_path == None :
            image_path=0
        info=Newcomments()
        info.image_path=image_path
        info.user_name=name
        info.com=a.com
        info.date=a.createddate
        new_comments.append(info)
    uerloginflag = 0        #是否有用户登录
    commentflag = 0         #说明评论是否成功
    if 'username' in request.session :
        uerloginflag=1
    if ('username' in request.session)and request.method == "POST":
        comment=request.POST.get("comment")
        username=request.session['username']
        u = User.objects.get(user__username=username)
        newcomment=CourseCom()
        newcomment.courseid=course
        newcomment.com=comment
        newcomment.user_name=username
        newcomment.save()
        commentflag=1
    return render(request,'course/coursedes.html',{"course":course,"teacherList":teachers,"des":des,"school":school,
                                                   "type":type,"flag":flag,"userflag":uerloginflag,
                                                   "commentflag":commentflag,"comments":new_comments})


