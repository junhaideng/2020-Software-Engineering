"""
author: Edgar
对课程相关的数据库进行管理
"""
from django.contrib import admin
from .models import *


class AdminCourse(admin.ModelAdmin):
    list_display = ("name", "type", "major","school")   # 显示的内容
    list_per_page = 30  # 每页的数据量
    ordering = ("name",)  # 排序方式
    search_fields = ("name",)  # 搜索框可以到哪些field进行搜索


class AdminCourseDes(admin.ModelAdmin):
    list_display = ("user_id", "course_id","des")
    list_per_page = 30
    ordering = ("user_id",)
    search_fields = ("des",)


class AdminTeacher(admin.ModelAdmin):
    list_display = ("name", "course_id")
    list_per_page = 30
    ordering = ("name", )
    search_fields = ("name",)

class AdminComment(admin.ModelAdmin):
    list_display = ("courseid", "user_name","com","createddate")
    list_per_page = 30
    ordering = ("courseid",)
    search_fields = ("courseid",)

admin.site.register(CourseCom, AdminComment)
admin.site.register(Course, AdminCourse)
admin.site.register(CourseDes, AdminCourseDes)
admin.site.register(TeacherOfCourse, AdminTeacher)
