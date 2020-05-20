"""
author: Edgar
对社区路由下的子路由进行配置
"""
from django.urls import path
from .views import *

app_name = "community"
urlpatterns = [
    path("", index, name='index'),  # 社区的主页
    path("post/<int:id>", detail, name='detail'),  # 每个帖子的详情页
    path("post/reply", reply, name="reply"),  # 提交回答
    path("post/comment", comment, name="comment"),  # 进行回复
]
