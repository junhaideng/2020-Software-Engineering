"""
author: Edgar
课程路由下的页面显示
TODO: 如何显示课程，怎么样显示
"""
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from user.models import ExpData
import time
import os


def index(request):
    """课程界面的首页"""
    return render(request, 'course/index.html')

