"""
author: Edgar
对社区界面的处理，包括社区界面的主页，分页，以及跳转到相对应的帖子详情页
"""

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from post.models import Post, PostComment, PostReply
from user.models import User
from django.core.paginator import Paginator
from math import ceil
from django.http.response import JsonResponse


def index(request):
    """社区首页"""
    posts = Post.objects.all()  # 获取所有的帖子
    per_page_num = 10  # 每一页的帖子数
    p = Paginator(posts, per_page_num)  # 分页对象
    total = ceil(posts.count() / per_page_num) * 10  # 总共页数， *10 是为了适应在layui中的显示(count变量)
    curr_page = 1  # 默认的时候指定的是第一页
    if request.GET.get("page"):  # 如果url中含有参数page，那么指定其页数 (?page=num)
        curr_page = request.GET.get("page")
    post = p.page(curr_page)  # 获取当前页面的信息
    return render(request, 'community/index.html', context={"posts": post, "curr_page": curr_page, "total": total})


def detail(request, id):
    """帖子详情"""
    post = Post.objects.get(id=id)  # 获取对应的帖子，为 Post 数据库模型
    post.counter += 1  # 阅读次数加一
    post.save()
    if post:
        reply = PostReply.objects.filter(post_id=id)  # 主回复内容  为PostReply 数据库模型  中间包含对于该帖子所有的第一层上的回复信息
        data = []  # 返回页面的信息
        for i in reply:
            """
            reply -> 该条回答
            user -> 写回答的用户
            comment -> 回复的信息
            """
            data.append({"user": User.objects.get(user_id=i.post_user_id), "reply": i,
                         "comments": PostComment.objects.filter(reply_id=i.id).order_by("-created_date")})
        return render(request, 'community/detail.html',
                      context={"post": post, "data": data, "total": reply.count()})
    else:
        return HttpResponse("404")


@require_http_methods(["POST"])  # 仅允许 POST方法
def reply(request):
    """对帖子进行回答"""
    user_id = request.user.id
    post_id = request.POST.get("id")  # 帖子对应的id
    content = request.POST.get("content")
    try:
        reply = PostReply(post_user_id=user_id, post_id=post_id, content=content)
        reply.save()
    except Exception as e:
        print(e)
        return JsonResponse({"status": 400, "message": "回答失败，请重新尝试"})
    else:
        return JsonResponse({"status": 200, "message": "回答成功"})


@require_http_methods(["POST"])  # 仅允许 POST方法
def comment(request):
    """对回答进行回复"""
    content = request.POST.get("content")
    id = request.POST.get("id")  # reply的id
    try:
        comment = PostComment(reply_id=id, commenter_id=request.user.id, content=content)  # 创建回复
        comment.save()
    except Exception as e:
        print(e)
        return JsonResponse({"status": 400, "message": "评论失败，请重新尝试"})
    else:
        return JsonResponse({"status": 200, "message": "评论成功"})


def get_hot(request):
    host = Post.objects.all().order_by("-counter")[:10]
    data = list(map(lambda x: {"topic": x.topic, "id": x.id}, host))
    return JsonResponse({"data": data})
