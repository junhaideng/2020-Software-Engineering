"""
author: Edgar
帖子相关的主要数据库
"""
from django.db import models
from django.utils import timezone


class Post(models.Model):
    """发帖的主要信息，不包括回复内容"""
    topic = models.CharField(max_length=100)  # 发帖主题
    counter = models.IntegerField()  # 浏览次数
    author_user_id = models.IntegerField()  # 发贴用户的id
    content = models.TextField()  # 帖子的内容
    created_time = models.DateTimeField(default=timezone.now)  # 发表的时间
    course = models.CharField(max_length=100)  # 所属课程

    class Meta:
        ordering = ("-created_time", )

    def __str__(self):
        return self.topic


class PostReply(models.Model):
    """回复的主要信息，不包括回复的回复，相当于在用户帖子下的一个新回复"""
    post_id = models.IntegerField()  # 帖子id, django自动生成的
    post_user_id = models.IntegerField()  # 对应回复用户的id，相当于一个新的回复
    content = models.TextField()  # 回复的内容
    created_date = models.DateTimeField(default=timezone.now)  # 回复的时间
    if_read = models.BooleanField(default=False)  # 是否已读

    class Meta:
        ordering = ("-created_date",)  # 按照时间的降序排


class PostComment(models.Model):
    """comment 是第二层的回复信息"""
    reply_id = models.IntegerField()  # reply 的 id  reply id 即可确定是哪一个 reply
    commenter_id = models.IntegerField()  # 谁回复的
    content = models.TextField()  # 回复的内容
    created_date = models.DateTimeField(default=timezone.now)  # 时间
    if_read = models.BooleanField(default=False)  # 是否已读

    class Meta:
        ordering = ("-created_date", )
