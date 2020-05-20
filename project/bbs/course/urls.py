from django.urls import path
from .views import *

app_name = "course"
urlpatterns = [
    path("", index, name='index'),
    path("upload/", upload, name='upload'),
    path("details/<str:type>/<str:school>/<int:page_num>", details, name='details'),
    path("coursedes/<int:pk>", coursedes, name='coursedes'),
    path("get_all_course/", get_all_course, name="get_all"),  # 获取所有的课程
]
