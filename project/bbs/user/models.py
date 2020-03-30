"""
author: Edgar
用户相关的数据库模型
"""
from django.db import models
from django.contrib.auth.models import User as AuthUser
from django.utils import timezone

GRADES = (('FR', '大一'),
          ('SO', '大二'),
          ('JR', '大三'),
          ('SR', '大四'),
          ("OT", '其他'),
          ("UN", "未知")
          )


class User(models.Model):
    """用户数据库"""
    user = models.OneToOneField(AuthUser, on_delete=models.CASCADE)  # 与django自带的User进行连接
    sex = models.BooleanField(default=True, blank=True, null=True)  # 性别 男 -> True
    profile = models.CharField(max_length=100, null=True, blank=True)  # 头像路径  可以为空
    academy = models.CharField(max_length=40, null=True, blank=True)  # 学院名  可以为空
    grade = models.CharField(choices=GRADES, max_length=30, default="UN", blank=True, null=True)  # 年级

    def __str__(self):
        return self.user.username


class ExpData(models.Model):
    """实验数据"""
    user_id = models.IntegerField()  # 上传文件的用户
    course_id = models.IntegerField()  # 与之有关的课程id
    date = models.DateTimeField(default=timezone.now)  # 上传文件的时间
    download_times = models.IntegerField()  # 下载次数
    path = models.CharField(max_length=100)  # 实验数据的路径, 路径下的文件名需要进行一下处理，以免冲突
    name = models.CharField(max_length=40)  # 实验数据的名称

    def __str__(self):
        return self.name
