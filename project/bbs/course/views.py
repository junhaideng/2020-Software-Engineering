from django.shortcuts import render


def index(request):
    """课程界面的首页"""
    return render(request, 'course/index.html')
