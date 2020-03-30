"""
author: Edgar
对社区界面的处理，包括社区界面的主页，分页，以及跳转到相对应的帖子详情页
TODO: 显示内容设计
"""

from django.http import HttpResponse
from django.shortcuts import render
from post.models import Post, PostComment, PostReply
from user.models import User
from django.core.paginator import Paginator
from math import ceil


def index(request):
    """社区首页"""
    posts = Post.objects.all()  # 获取所有的帖子
    per_page_num = 1  # 每一页的帖子数
    p = Paginator(posts, per_page_num)  # 分页对象
    total = ceil(posts.count() / per_page_num) * 10  # 总共页数， *10 是为了适应在layui中的显示(count变量)
    curr_page = 1  # 默认的时候指定的是第一页
    if request.GET.get("page"):  # 如果url中含有参数page，那么指定其页数 (?page=num)
        curr_page = request.GET.get("page")
    page = p.page(curr_page)  # 获取当前页面的信息
    return render(request, 'community/index.html', context={"posts": page, "curr_page": curr_page, "total": total})


def detail(request, id):
    """帖子详情"""
    post = Post.objects.get(id=id)  # 获取对应的帖子，为 Post 数据库模型
    if post:
        reply = PostReply.objects.filter(post_id=id)  # 主回复内容  为PostReply 数据库模型  中间包含对于该帖子所有的第一层上的回复信息
        data = []  # 返回页面的信息
        for i in reply:
            data.append({"user": User.objects.get(user_id=i.post_user_id), "reply": i,
                         "comments": PostComment.objects.filter(post_id=id, detail_id=i.id).order_by("date")})

        return render(request, 'community/detail.html',
                      context={"post": post, "data": data, "total": reply.count()})
    else:
        return HttpResponse("404")
