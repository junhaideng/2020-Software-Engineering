"""bbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.views import static
from django.contrib import admin
from django.urls import path, include, re_path
from search.views import files

urlpatterns = [
    path('admin/', admin.site.urls),  # 管理路由
    path("", include("home.urls")),  # 主页
    path("course/", include("course.urls")),  # 课程路由
    path("search/", include("search.urls")),  # 搜索路由
    path("post/", include("post.urls")),  # 发帖路由
    path("user/", include("user.urls")),  # 用户相关路由
    path("community/", include("community.urls")),  # 社区相关路由
    path("feedback/", include("feedback.urls")),  # 反馈路由
    path("download/", files, name="file"),  # 文件下载路由,
    # Debug为False的时候应该使用：
    re_path(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),  # 静态加载文件
    re_path(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}, name='media'),  # 媒体文件
]
