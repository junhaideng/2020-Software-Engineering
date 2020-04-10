from django.urls import path
from .views import *
app_name = "user"
urlpatterns = [
    path("login/", login, name='login'),  # 负责用户的登录
    path("signup/", signup, name='signup'),  # 负责用户的注册
    path("forget/", forget, name='forget'),  # 负责密码的找回，先输入用户名 验证用户存在
    path("forgetdetail/", forgetdetail, name='forgetdetail'),  # 负责密保验证
    path("logout/", logout, name='logout'),  # 负责用户的登出
    path("profile/", profile, name='profile'),  # 负责显示用户的个人资料
    path("history/", history, name="history"),  # 发帖记录
    path("file/", file, name='file'),  # 用户上传的文件
    path("resetpwd/", resetpwd, name='resetpwd')  # 修改密码
]