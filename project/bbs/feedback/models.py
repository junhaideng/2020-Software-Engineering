"""
author: Edgar
反馈界面的主要数据库模型
"""
from django.db import models


class Feedback(models.Model):
    user_id = models.IntegerField()  # 用户id
    username = models.CharField(max_length=30)  # 用户名
    subject = models.CharField(max_length=100)  # 主题
    content = models.TextField()  # 反馈内容
    feedback_type = models.BooleanField(default=True)  # True -> 建议  False -> 举报

    class Meta:
        ordering = ("username", )

    def __str__(self):
        return self.subject

