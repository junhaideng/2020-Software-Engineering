"""
author: Edgar
自定义过滤器，每添加一个请重启服务器，系统不会自动重新加载这些
官方参考链接： https://docs.djangoproject.com/zh-hans/3.0/howto/custom-template-tags/
"""
from django import template
from user.models import User
register = template.Library()


@register.filter(name="getNameFromId")
def get_name_from_id(value):
    """根据id获取用户的用户名"""
    try:
        return User.objects.get(id=value).user.username
    except:
        return None


@register.filter(name="getProfileFromId")
def get_profile_from_id(value):
    """根据id获取用户的头像信息"""
    try:
        return User.objects.get(id=value).profile
    except:
        return None


@register.filter(name="getProfileFromAuthId")
def get_profile_from_auth_id(value):
    """从django中默认的user id中获取到与之对应的profile"""
    try:
        return User.objects.get(user_id=value).profile
    except:
        return None
