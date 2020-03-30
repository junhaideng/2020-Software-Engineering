"""
author: Edgar
对反馈界面的显示进行处理
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from user.models import User
from .models import Feedback


@login_required
def index(request):
    """反馈界面"""
    if request.method == "POST":
        subject = request.POST.get("subject")
        content = request.POST.get("content")
        feedback_type = bool(int(request.POST.get("type")))
        message = None
        if not subject.strip():
            message = {"info": '主题为空', 'tag': "warning"}
        if not content.strip():
            message = {"info": "内容为空", 'tag': "warning"}
        if content.strip() and subject.strip():
            message = {"info": "反馈成功, 请等待管理员处理", "tag": "success"}
            feedback = Feedback(user_id=User.objects.get(user_id=request.user.id).id,
                                username=request.user.username,
                                subject=subject,
                                content=content,
                                feedback_type=feedback_type)  # 对数据库的属性进行赋值
            feedback.save()  # 插入到数据库
        request.session["feedback_message"] = message  # 将信息保存到session中，这里如果不使用session，比较难实现对用户成功操作进行提示
        return redirect(reverse("feedback:index"))  # 重新重定向到反馈界面，如果不是重定向，刷新的时候容易使得表单进行重新提交
    if "feedback_message" in request.session.keys():  # 如果session中存在
        message = request.session.pop("feedback_message")
    else:
        message = None
    return render(request, "feedback/index.html", context={"message": message})
