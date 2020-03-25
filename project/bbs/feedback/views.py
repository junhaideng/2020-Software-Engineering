from django.shortcuts import render


def index(request):
    """反馈界面"""
    return render(request, 'feedback/index.html')
