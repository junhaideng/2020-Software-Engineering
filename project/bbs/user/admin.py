"""
author: Edgar
对user下的数据库模型进行管理
"""
from django.contrib import admin
from .models import *


class AdminUser(admin.ModelAdmin):
    list_display = ("user", "sex", "academy", "grade")  # 显示信息
    ordering = ("user",)  # 排序信息
    list_per_page = 30  # 每页显示的数据量
    search_fields = ("user", "academy")  # 搜索区域


admin.site.register(User, AdminUser)


