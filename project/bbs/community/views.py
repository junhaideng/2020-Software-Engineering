from django.shortcuts import render


def index(request):
    """社区首页"""
    return render(request, 'community/index.html')
