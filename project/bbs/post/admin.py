"""
author: Edgar
对应用post下的数据库在admin界面进行管理注册
"""

from django.contrib import admin
from .models import *


class AdminPost(admin.ModelAdmin):
    """对数据库Post在admin进行管理"""
    list_display = ("topic", "counter", "content", "created_time")  # 显示的属性
    list_per_page = 30  # 每页的数据数
    ordering = ("-created_time", "topic")  # 排列方式
    search_fields = ("topic",)  # 搜索区可以搜到哪些区域


admin.site.register(Post, AdminPost)  # 进行注册
