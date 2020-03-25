from django.urls import path
from .views import *
app_name = "user"
urlpatterns = [
    path("login/", login, name='login'),  # 负责用户的登录
    path("signup/", signup, name='signup'),  # 负责用户的注册
    path("forget/", forget, name='forget'),  # 负责密码的找回
]