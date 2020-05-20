"""
author: Edgar
发帖界面, 负责用户帖子的上传，页面的展示
TODO: 发帖界面的美化
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from post.models import Post
from django.http import JsonResponse
from course.models import Course



@login_required
def index(request):
    """发帖的界面"""
    if request.method == "POST":  # 如果请求方式为POST, 则为提交内容
        topic = request.POST.get("topic")  # 主题
        course = request.POST.get("course")
        content = request.POST.get("content")  # 内容
        print(request.POST)

        if topic and course and content:
            post = Post(topic=topic, course=course, counter=0, author_user_id=request.user.id, content=content)  # 数据库插入
            post.save()
            request.session["status"] = "提交成功"
            return JsonResponse({"status": "提交成功", "code": 200})
        else:
            if not topic:
                return JsonResponse({"status": "标题不能为空", "code": 400})
            elif not course:
                return JsonResponse({'status': '请选择对应的课程', "code": 400})
            else:
                return JsonResponse({"status": "请输入内容", "code": 400})

    course = Course.objects.all()
    data = []
    for c in course:
        data.append(c.name)
    status = None
    if request.session.get("status"):
        status = request.session.pop("status")
    print(status)
    return render(request, "post/index.html", context={"data": data, "msg": status})


