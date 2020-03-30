"""
author: Edgar
发帖界面, 负责用户帖子的上传，页面的展示
TODO: 发帖界面的美化
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from post.models import Post


@login_required
@csrf_exempt
def index(request):
    """发帖的界面"""
    if request.method == "POST":  # 如果请求方式为POST, 则为提交内容
        topic = request.POST.get("topic")  # 主题
        content = request.POST.get("content")  # 内容
        post = Post(topic=topic, counter=1, author_user_id=1, content=content)  # 数据库插入
        post.save()
    return render(request, "post/index.html")
